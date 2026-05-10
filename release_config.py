from __future__ import annotations

from pathlib import Path

APP_NAME = "Excel2Json"
APP_VERSION = "0.4.0"
RELEASES_DIRNAME = "Releases"
VERSION_PREFIX = "v"


def get_version_tag() -> str:
    return f"{VERSION_PREFIX}{APP_VERSION}"


def get_release_root(base_dir: Path) -> Path:
    return base_dir / RELEASES_DIRNAME


def get_version_release_dir(base_dir: Path) -> Path:
    return get_release_root(base_dir) / get_version_tag()


def get_build_artifacts_dir(base_dir: Path) -> Path:
    return get_release_root(base_dir) / "_build"
