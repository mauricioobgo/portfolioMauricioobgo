from __future__ import annotations

import argparse
import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


DEFAULT_WEB_ROOT = Path("build/web")
BUNDLE_RELATIVE_PATH = Path("assets/app/app.zip")
PYTHON_WORKER_RELATIVE_PATH = Path("python-worker.js")
PYTHON_LOADER_RELATIVE_PATH = Path("python.js")
FLUTTER_BOOTSTRAP_RELATIVE_PATH = Path("flutter_bootstrap.js")
FONTS_RELATIVE_PATH = Path("assets/fonts")
SOURCE_FONTS_DIR = Path("src/assets/fonts")

RUNTIME_MODULES = ("flet", "flet_lottie", "msgpack")
RUNTIME_FILES = ("repath.py", "six.py")
REQUIRED_BUNDLE_ENTRIES = (
    "main.py",
    "flet/__init__.py",
    "flet_lottie/__init__.py",
    "msgpack/__init__.py",
    "repath.py",
    "six.py",
)

# Flet's stock python-worker.js has the JS fetch+unpackArchive hook in the
# top-level ``self.initPyodide`` body. PR #42 used to remove that hook and
# replace the Python-side archive download with a no-op (relying on the JS
# side to do the unpack). The JS-side path is broken on Pyodide's MEMFS
# (``shutil.unpack_archive`` falls over on a JS-supplied ``ArrayBuffer``),
# so we now keep the stock JS hook and ensure the original Python-side
# ``pyfetch(...).unpack_archive()`` flow runs.
WORKER_JS_HOOK_OLD = """        flet_js.documentUrl = documentUrl;
        const pyArgs = self.flet_js.args || {};
        if (!("script" in pyArgs)) {
            const appPackageUrl = new URL(
                pyArgs["app_package_url"] || self.appPackageUrl || "assets/app/app.zip",
                self.documentUrl || self.location.href
            ).toString();
            console.log("Downloading app archive");
            const archiveResponse = await fetch(appPackageUrl);
            if (!archiveResponse.ok) {
                throw new Error(`Unable to fetch app archive: ${archiveResponse.status} ${archiveResponse.statusText}`);
            }
            const archiveBuffer = await archiveResponse.arrayBuffer();
            self.pyodide.unpackArchive(archiveBuffer, "zip");
        }
        await self.pyodide.runPythonAsync(`
"""
WORKER_JS_HOOK_NEW = (
    "        flet_js.documentUrl = documentUrl;\n        await self.pyodide.runPythonAsync(`\n"
)
WORKER_JS_HOOK_MARKER = 'self.pyodide.unpackArchive(archiveBuffer, "zip");'
WORKER_ARCHIVE_BLOCK_OLD = """        if "script" in py_args:
            print("Saving script to a file")
            with open(f"{python_module_name}.py", "w") as f:
                f.write(py_args["script"]);
"""
WORKER_ARCHIVE_BLOCK_NEW = """        if "script" not in py_args:
            print("Downloading app archive")
            response = await pyfetch(app_package_url)
            await response.unpack_archive()
        else:
            print("Saving script to a file")
            with open(f"{python_module_name}.py", "w") as f:
                f.write(py_args["script"]);
"""
PYTHON_LOADER_READY_OLD = """    } else {
        console.log(`Python worker initialized: ${appId}`);
    }
"""
PYTHON_LOADER_READY_NEW = """    } else {
        if (typeof globalThis.removeSplashFromWeb === "function") {
            globalThis.removeSplashFromWeb();
        }
        console.log(`Python worker initialized: ${appId}`);
    }
"""
PYTHON_LOADER_PATCH_MARKER = "globalThis.removeSplashFromWeb();"
FLUTTER_BUILD_CONFIG_PREFIX = "_flutter.buildConfig = "


@dataclass(frozen=True)
class PatchSummary:
    bundle_entries_added: int
    worker_patched: bool
    python_loader_patched: bool
    bootstrap_patched: bool
    fonts_copied: int


def _module_root(module_name: str) -> Path:
    spec = importlib.util.find_spec(module_name)
    if spec is None or spec.origin is None:
        raise RuntimeError(f"Unable to locate module {module_name!r} in the current environment.")
    origin = Path(spec.origin).resolve()
    if origin.name == "__init__.py":
        return origin.parent
    return origin


def _iter_runtime_sources() -> list[tuple[Path, str]]:
    sources: list[tuple[Path, str]] = []
    for module_name in RUNTIME_MODULES:
        source_root = _module_root(module_name)
        if source_root.is_dir():
            for path in source_root.rglob("*"):
                if path.is_dir() or "__pycache__" in path.parts:
                    continue
                if path.suffix in {".pyc", ".pyd", ".so", ".dll"}:
                    continue
                arcname = str(Path(module_name) / path.relative_to(source_root)).replace("\\", "/")
                sources.append((path, arcname))
        else:
            sources.append((source_root, source_root.name))

    for filename in RUNTIME_FILES:
        source_path = _module_root(filename.removesuffix(".py"))
        if source_path.is_dir():
            raise RuntimeError(f"Expected file module for {filename!r}, found directory.")
        sources.append((source_path, filename))

    return sources


def _web_root_from_input(value: str) -> Path:
    path = Path(value).resolve()
    if path.name == "app.zip":
        return path.parents[2]
    return path


def _replace_once(text: str, old: str, new: str, *, label: str) -> tuple[str, bool]:
    if new in text:
        return text, False
    if old not in text:
        raise RuntimeError(f"Unable to find {label} while patching generated web assets.")
    return text.replace(old, new, 1), True


def patch_bundle(bundle_path: Path) -> int:
    if not bundle_path.exists():
        raise FileNotFoundError(f"Bundle not found: {bundle_path}")

    added = 0
    with ZipFile(bundle_path, "a", compression=ZIP_DEFLATED) as archive:
        existing = set(archive.namelist())
        for source_path, arcname in _iter_runtime_sources():
            if arcname in existing:
                continue
            archive.write(source_path, arcname)
            added += 1
    return added


def patch_python_worker(worker_path: Path) -> bool:
    if not worker_path.exists():
        raise FileNotFoundError(f"Python worker not found: {worker_path}")

    content = worker_path.read_text(encoding="utf-8")
    original = content

    # Drop the JS-side ``fetch + unpackArchive`` block that PR #42 added. The
    # MEMFS-backed Pyodide that Flet ships cannot seek inside the temp file
    # produced from a JS ``ArrayBuffer``; the unpack raises EINVAL and the
    # site stays blank. Restoring the original 2-line ``documentUrl`` /
    # ``runPythonAsync`` opener lets the Python-side ``pyfetch`` flow below
    # do the unpacking instead.
    content, js_hook_changed = _replace_once(
        content,
        WORKER_JS_HOOK_OLD,
        WORKER_JS_HOOK_NEW,
        label="worker JS archive hook",
    )

    # Restore the Python-side archive download. PR #42 reduced this branch
    # to a script-only no-op because it expected the JS hook above to have
    # already unpacked ``app.zip``. Without the JS hook, ``main.py`` is
    # never extracted from ``app.zip`` and ``runpy`` fails.
    content, archive_block_changed = _replace_once(
        content,
        WORKER_ARCHIVE_BLOCK_OLD,
        WORKER_ARCHIVE_BLOCK_NEW,
        label="worker archive block",
    )

    if content != original:
        worker_path.write_text(content, encoding="utf-8")

    return js_hook_changed or archive_block_changed


def patch_python_loader(loader_path: Path) -> bool:
    if not loader_path.exists():
        raise FileNotFoundError(f"Python loader not found: {loader_path}")

    content = loader_path.read_text(encoding="utf-8")
    updated, changed = _replace_once(
        content,
        PYTHON_LOADER_READY_OLD,
        PYTHON_LOADER_READY_NEW,
        label="python loader ready hook",
    )
    if changed:
        loader_path.write_text(updated, encoding="utf-8")
    return changed


def patch_flutter_bootstrap(bootstrap_path: Path) -> bool:
    if not bootstrap_path.exists():
        raise FileNotFoundError(f"Flutter bootstrap not found: {bootstrap_path}")

    content = bootstrap_path.read_text(encoding="utf-8")
    newline = "\r\n" if "\r\n" in content else "\n"
    lines = content.splitlines()

    for index, line in enumerate(lines):
        if not line.startswith(FLUTTER_BUILD_CONFIG_PREFIX):
            continue

        json_text = line.removeprefix(FLUTTER_BUILD_CONFIG_PREFIX)
        if not json_text.endswith(";"):
            raise RuntimeError("Unable to parse _flutter.buildConfig from flutter_bootstrap.js.")

        build_config = json.loads(json_text.removesuffix(";"))
        builds = build_config.get("builds")
        if not isinstance(builds, list):
            raise RuntimeError("flutter_bootstrap.js does not expose a valid builds list.")

        js_builds = [build for build in builds if build.get("compileTarget") == "dart2js"]
        if not js_builds:
            raise RuntimeError("flutter_bootstrap.js does not expose a dart2js build to keep.")

        build_config["builds"] = js_builds
        updated_line = (
            f"{FLUTTER_BUILD_CONFIG_PREFIX}{json.dumps(build_config, separators=(',', ':'))};"
        )
        changed = updated_line != line
        lines[index] = updated_line
        if changed:
            bootstrap_path.write_text(newline.join(lines) + newline, encoding="utf-8")
        return changed

    raise RuntimeError("Unable to find _flutter.buildConfig in flutter_bootstrap.js.")


def copy_fonts(web_root: Path) -> int:
    """Copy the project custom fonts (Poppins / IBMPlexMono) into the built site.

    Flet's `flet build web` only copies Flutter's default fonts into
    ``build/web/assets/fonts/``. The deployed ``index.html`` exposes
    ``fontFallbackBaseUrl: "assets/fonts/"`` and the running Flet app
    references ``fonts/Poppins-Regular.ttf`` etc. via ``page.fonts`` —
    those references 404 in production, which can cause Flet to render an
    empty page on GitHub Pages.

    Returns the number of font files copied.
    """
    source_dir = SOURCE_FONTS_DIR
    target_dir = web_root / FONTS_RELATIVE_PATH
    if not source_dir.is_dir():
        # No custom fonts declared for this project — nothing to do.
        return 0

    target_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for source in sorted(source_dir.iterdir()):
        if not source.is_file():
            continue
        if source.suffix.lower() not in {".ttf", ".otf"}:
            continue
        destination = target_dir / source.name
        if destination.exists() and destination.read_bytes() == source.read_bytes():
            continue
        destination.write_bytes(source.read_bytes())
        copied += 1
    return copied


def verify_fonts(web_root: Path) -> None:
    """Ensure every source font ends up in the built site."""
    source_dir = SOURCE_FONTS_DIR
    if not source_dir.is_dir():
        return
    target_dir = web_root / FONTS_RELATIVE_PATH
    missing = [
        source.name
        for source in sorted(source_dir.iterdir())
        if source.is_file()
        and source.suffix.lower() in {".ttf", ".otf"}
        and not (target_dir / source.name).is_file()
    ]
    if missing:
        raise RuntimeError(
            f"Built web bundle is missing custom fonts: {missing}. "
            "patch_web_bundle.copy_fonts should have copied them."
        )


def verify_bundle(bundle_path: Path) -> None:
    if not bundle_path.exists():
        raise FileNotFoundError(f"Bundle not found: {bundle_path}")

    with ZipFile(bundle_path) as archive:
        entries = set(archive.namelist())

    missing = [entry for entry in REQUIRED_BUNDLE_ENTRIES if entry not in entries]
    if missing:
        raise RuntimeError(f"Generated app bundle is missing required runtime entries: {missing}")


def verify_python_worker(worker_path: Path) -> None:
    if not worker_path.exists():
        raise FileNotFoundError(f"Python worker not found: {worker_path}")

    content = worker_path.read_text(encoding="utf-8")
    if WORKER_JS_HOOK_MARKER in content:
        raise RuntimeError(
            "python-worker.js still uses the broken JS-side "
            f"{WORKER_JS_HOOK_MARKER!r} hook. The JS-side unpack path is "
            "broken on Pyodide's MEMFS and was removed in the PR #42 revert."
        )
    if "response.unpack_archive()" not in content:
        raise RuntimeError(
            "python-worker.js is missing the Python-side "
            "`response.unpack_archive()` flow that extracts app.zip. Without "
            "it, runpy cannot find main.py and the site stays blank."
        )


def verify_python_loader(loader_path: Path) -> None:
    if not loader_path.exists():
        raise FileNotFoundError(f"Python loader not found: {loader_path}")

    content = loader_path.read_text(encoding="utf-8")
    if PYTHON_LOADER_PATCH_MARKER not in content:
        raise RuntimeError("python.js is missing the splash removal hook after worker init.")


def verify_flutter_bootstrap(bootstrap_path: Path) -> None:
    if not bootstrap_path.exists():
        raise FileNotFoundError(f"Flutter bootstrap not found: {bootstrap_path}")

    content = bootstrap_path.read_text(encoding="utf-8")
    forbidden_tokens = ('"compileTarget":"dart2wasm"', '"renderer":"skwasm"', "main.dart.wasm")
    for token in forbidden_tokens:
        if token in content:
            raise RuntimeError(
                f"flutter_bootstrap.js still advertises the WASM startup path: {token}"
            )
    if '"mainJsPath":"main.dart.js"' not in content:
        raise RuntimeError("flutter_bootstrap.js is missing the JS entrypoint declaration.")


def verify_web_build(web_root: Path) -> None:
    verify_bundle(web_root / BUNDLE_RELATIVE_PATH)
    verify_python_worker(web_root / PYTHON_WORKER_RELATIVE_PATH)
    verify_python_loader(web_root / PYTHON_LOADER_RELATIVE_PATH)
    verify_flutter_bootstrap(web_root / FLUTTER_BOOTSTRAP_RELATIVE_PATH)
    verify_fonts(web_root)


def patch_web_build(web_root: Path) -> PatchSummary:
    bundle_path = web_root / BUNDLE_RELATIVE_PATH
    worker_path = web_root / PYTHON_WORKER_RELATIVE_PATH
    loader_path = web_root / PYTHON_LOADER_RELATIVE_PATH
    bootstrap_path = web_root / FLUTTER_BOOTSTRAP_RELATIVE_PATH

    bundle_entries_added = patch_bundle(bundle_path)
    worker_patched = patch_python_worker(worker_path)
    python_loader_patched = patch_python_loader(loader_path)
    bootstrap_patched = patch_flutter_bootstrap(bootstrap_path)
    fonts_copied = copy_fonts(web_root)
    verify_web_build(web_root)
    return PatchSummary(
        bundle_entries_added=bundle_entries_added,
        worker_patched=worker_patched,
        python_loader_patched=python_loader_patched,
        bootstrap_patched=bootstrap_patched,
        fonts_copied=fonts_copied,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Patch and verify the generated Flet static web bundle for GitHub Pages."
    )
    parser.add_argument(
        "web_root",
        nargs="?",
        default=str(DEFAULT_WEB_ROOT),
        help="Path to the generated build/web directory. For backward compatibility, app.zip is also accepted.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    web_root = _web_root_from_input(args.web_root)
    summary = patch_web_build(web_root)
    print(
        f"Patched {web_root} with {summary.bundle_entries_added} runtime files; "
        f"python-worker.js updated={summary.worker_patched}; "
        f"python.js updated={summary.python_loader_patched}; "
        f"flutter_bootstrap.js updated={summary.bootstrap_patched}; "
        f"{summary.fonts_copied} custom font(s) copied."
    )


if __name__ == "__main__":
    main()
