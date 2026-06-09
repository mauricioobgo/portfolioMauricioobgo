from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from portfolio_app.scripts import patch_web_bundle


def _write_bundle(path: Path, entries: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        for name, content in entries.items():
            archive.writestr(name, content)


def _read_worker_fixture() -> str:
    return """self.pyodideUrl = null;
self.appPackageUrl = null;
self.micropipIncludePre = false;
self.pythonModuleName = null;
self.documentUrl = null;
self.initialized = false;
self.flet_js = {}; // namespace for Python global functions

self.initPyodide = async function () {
    try {
        importScripts(self.pyodideUrl);
        self.pyodide = await loadPyodide();
        self.pyodide.registerJsModule("flet_js", flet_js);
        self.pyodide.globals.set("app_package_url", self.appPackageUrl);
        self.pyodide.globals.set("python_module_name", self.pythonModuleName);
        self.pyodide.globals.set("micropip_include_pre", self.micropipIncludePre);
        flet_js.documentUrl = documentUrl;
        await self.pyodide.runPythonAsync(`
        import flet_js, os, runpy, sys, traceback
        from pyodide.http import pyfetch

        py_args = flet_js.args.to_py() if flet_js.args else None

        if "app_package_url" in py_args:
            app_package_url = py_args["app_package_url"]

        if app_package_url is None:
            app_package_url = "assets/app/app.zip"

        if "python_module_name" in py_args:
            python_module_name = py_args["python_module_name"]

        if python_module_name is None:
            python_module_name = "main"

        if "micropip_include_pre" in py_args:
            micropip_include_pre = py_args["micropip_include_pre"]

        if micropip_include_pre is None:
            micropip_include_pre = False

        print("python_module_name:", python_module_name)
        print("micropip_include_pre:", micropip_include_pre)

        if "script" not in py_args:
            print("Downloading app archive")
            response = await pyfetch(app_package_url)
            await response.unpack_archive()
        else:
            print("Saving script to a file")
            with open(f"{python_module_name}.py", "w") as f:
                f.write(py_args["script"]);

        pkgs_path = "__pypackages__"
        if os.path.exists(pkgs_path):
            print(f"Adding {pkgs_path} to sys.path")
            sys.path.insert(0, pkgs_path)

        async def ensure_micropip():
            try:
                import micropip
            except ImportError:
                import pyodide_js
                await pyodide_js.loadPackage("micropip")
                import micropip
            return micropip

        if os.path.exists("requirements.txt"):
            with open("requirements.txt", "r") as f:
                deps = []

        if "dependencies" in py_args:
            micropip = await ensure_micropip()
            await micropip.install(py_args["dependencies"], pre=micropip_include_pre)

        runpy.run_module(python_module_name, run_name="__main__")
      `);
        await self.flet_js.start_connection(self.receiveCallback);
        self.postMessage("initialized");
    } catch (error) {
        self.postMessage(error.toString());
    }
};
"""


def _write_runtime_files(tmp_path: Path) -> list[tuple[Path, str]]:
    runtime_dir = tmp_path / "runtime"
    files = {
        "main.py": "print('hello')\n",
        "flet/__init__.py": "__all__ = []\n",
        "flet_lottie/__init__.py": "__all__ = []\n",
        "msgpack/__init__.py": "__all__ = []\n",
        "repath.py": "def parse(path):\n    return path\n",
        "six.py": "__version__ = '1.17.0'\n",
    }
    sources: list[tuple[Path, str]] = []
    for arcname, content in files.items():
        source_path = runtime_dir / arcname
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_text(content, encoding="utf-8")
        sources.append((source_path, arcname))
    return sources


def test_patch_web_build_updates_worker_and_verifies_artifact(tmp_path, monkeypatch) -> None:
    web_root = tmp_path / "build" / "web"
    bundle_path = web_root / "assets" / "app" / "app.zip"
    worker_path = web_root / "python-worker.js"
    loader_path = web_root / "python.js"
    bootstrap_path = web_root / "flutter_bootstrap.js"

    _write_bundle(bundle_path, {"main.py": "print('app')\n"})
    worker_path.parent.mkdir(parents=True, exist_ok=True)
    worker_path.write_text(_read_worker_fixture(), encoding="utf-8")
    loader_path.write_text(
        "    } else {\n        console.log(`Python worker initialized: ${appId}`);\n    }\n",
        encoding="utf-8",
    )
    bootstrap_path.write_text(
        '_flutter.buildConfig = {"engineRevision":"demo","builds":[{"compileTarget":"dart2wasm","renderer":"skwasm","mainWasmPath":"main.dart.wasm","jsSupportRuntimePath":"main.dart.mjs"},{"compileTarget":"dart2js","renderer":"canvaskit","mainJsPath":"main.dart.js"}]};\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(
        patch_web_bundle,
        "_iter_runtime_sources",
        lambda: _write_runtime_files(tmp_path),
    )

    summary = patch_web_bundle.patch_web_build(web_root)

    assert summary.bundle_entries_added == 5
    assert summary.worker_patched is True
    assert summary.python_loader_patched is True
    assert summary.bootstrap_patched is True

    worker_content = worker_path.read_text(encoding="utf-8")
    assert 'self.pyodide.unpackArchive(archiveBuffer, "zip");' in worker_content
    assert "response.unpack_archive()" not in worker_content

    loader_content = loader_path.read_text(encoding="utf-8")
    assert "globalThis.removeSplashFromWeb();" in loader_content

    bootstrap_content = bootstrap_path.read_text(encoding="utf-8")
    assert '"compileTarget":"dart2wasm"' not in bootstrap_content
    assert '"mainJsPath":"main.dart.js"' in bootstrap_content

    with ZipFile(bundle_path) as archive:
        names = set(archive.namelist())

    assert set(patch_web_bundle.REQUIRED_BUNDLE_ENTRIES) <= names


def test_verify_web_build_rejects_wasm_bootstrap(tmp_path) -> None:
    web_root = tmp_path / "build" / "web"
    bundle_path = web_root / "assets" / "app" / "app.zip"
    worker_path = web_root / "python-worker.js"
    loader_path = web_root / "python.js"
    bootstrap_path = web_root / "flutter_bootstrap.js"

    _write_bundle(
        bundle_path,
        {
            "main.py": "print('app')\n",
            "flet/__init__.py": "__all__ = []\n",
            "flet_lottie/__init__.py": "__all__ = []\n",
            "msgpack/__init__.py": "__all__ = []\n",
            "repath.py": "def parse(path):\n    return path\n",
            "six.py": "__version__ = '1.17.0'\n",
        },
    )
    worker_path.parent.mkdir(parents=True, exist_ok=True)
    worker_path.write_text(
        "const archiveBuffer = await archiveResponse.arrayBuffer();\n"
        'self.pyodide.unpackArchive(archiveBuffer, "zip");\n',
        encoding="utf-8",
    )
    loader_path.write_text("globalThis.removeSplashFromWeb();\n", encoding="utf-8")
    bootstrap_path.write_text(
        '_flutter.buildConfig = {"builds":[{"compileTarget":"dart2wasm","renderer":"skwasm","mainWasmPath":"main.dart.wasm"}]};\n',
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="WASM startup path"):
        patch_web_bundle.verify_web_build(web_root)


def test_copy_fonts_copies_custom_fonts(tmp_path, monkeypatch) -> None:
    """copy_fonts pulls every .ttf/.otf from src/assets/fonts/ into the web root."""
    source_dir = tmp_path / "src" / "assets" / "fonts"
    source_dir.mkdir(parents=True)
    (source_dir / "Poppins-Regular.ttf").write_bytes(b"poppins-data")
    (source_dir / "IBMPlexMono-Medium.ttf").write_bytes(b"ibm-plex-data")
    # Non-font files should be ignored.
    (source_dir / "README.md").write_text("ignore me", encoding="utf-8")

    web_root = tmp_path / "build" / "web"

    monkeypatch.setattr(patch_web_bundle, "SOURCE_FONTS_DIR", source_dir)
    copied = patch_web_bundle.copy_fonts(web_root)

    assert copied == 2
    target = web_root / "assets" / "fonts"
    assert (target / "Poppins-Regular.ttf").read_bytes() == b"poppins-data"
    assert (target / "IBMPlexMono-Medium.ttf").read_bytes() == b"ibm-plex-data"
    assert not (target / "README.md").exists()


def test_copy_fonts_is_idempotent(tmp_path, monkeypatch) -> None:
    """Re-running copy_fonts with unchanged sources should copy zero new files."""
    source_dir = tmp_path / "src" / "assets" / "fonts"
    source_dir.mkdir(parents=True)
    (source_dir / "Poppins-Bold.ttf").write_bytes(b"bold")

    web_root = tmp_path / "build" / "web"

    monkeypatch.setattr(patch_web_bundle, "SOURCE_FONTS_DIR", source_dir)
    assert patch_web_bundle.copy_fonts(web_root) == 1
    # Second run: file already present with same bytes → no copy.
    assert patch_web_bundle.copy_fonts(web_root) == 0


def test_copy_fonts_handles_missing_source_dir(tmp_path, monkeypatch) -> None:
    """If the project has no custom fonts, copy_fonts is a no-op."""
    web_root = tmp_path / "build" / "web"
    monkeypatch.setattr(patch_web_bundle, "SOURCE_FONTS_DIR", tmp_path / "does-not-exist")
    assert patch_web_bundle.copy_fonts(web_root) == 0


def test_verify_fonts_flags_missing_fonts(tmp_path, monkeypatch) -> None:
    """verify_fonts raises when a source font is absent from the built site."""
    source_dir = tmp_path / "src" / "assets" / "fonts"
    source_dir.mkdir(parents=True)
    (source_dir / "Poppins-Regular.ttf").write_bytes(b"poppins")

    web_root = tmp_path / "build" / "web"
    web_root.mkdir(parents=True)
    # Built site is missing the custom font.
    empty_fonts = web_root / "assets" / "fonts"
    empty_fonts.mkdir(parents=True)
    (empty_fonts / "MaterialIcons-Regular.otf").write_bytes(b"default")

    monkeypatch.setattr(patch_web_bundle, "SOURCE_FONTS_DIR", source_dir)
    with pytest.raises(RuntimeError, match="Poppins-Regular.ttf"):
        patch_web_bundle.verify_fonts(web_root)
