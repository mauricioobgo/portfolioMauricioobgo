from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


RUNTIME_MODULES = ("flet", "flet_lottie", "msgpack")
RUNTIME_FILES = ("repath.py",)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inject required pure-Python runtime packages into a Flet web app.zip bundle."
    )
    parser.add_argument(
        "bundle",
        nargs="?",
        default="build/web/assets/app/app.zip",
        help="Path to the generated app.zip bundle.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bundle_path = Path(args.bundle).resolve()
    added = patch_bundle(bundle_path)
    print(f"Patched {bundle_path} with {added} runtime files.")


if __name__ == "__main__":
    main()
