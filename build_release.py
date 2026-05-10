from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from release_config import (
    APP_NAME,
    APP_VERSION,
    get_build_artifacts_dir,
    get_release_root,
    get_version_release_dir,
    get_version_tag,
)


def run_pyinstaller(base_dir: Path, build_dir: Path) -> Path:
    dist_dir = build_dir / "dist"
    work_dir = build_dir / "work"
    spec_dir = build_dir / "spec"

    for path in (dist_dir, work_dir, spec_dir):
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--console",
        "--name",
        APP_NAME,
        "--distpath",
        str(dist_dir),
        "--workpath",
        str(work_dir),
        "--specpath",
        str(spec_dir),
        str(base_dir / "main.py"),
    ]

    subprocess.run(command, cwd=base_dir, check=True)
    return dist_dir / f"{APP_NAME}.exe"


def write_release_launcher(release_dir: Path) -> None:
    launcher = "\n".join(
        [
            "@echo off",
            "setlocal",
            f"\"%~dp0{APP_NAME}.exe\"",
            "pause",
            "",
        ]
    )
    (release_dir / "gen_data.bat").write_text(launcher, encoding="utf-8")


def copy_release_documents(base_dir: Path, release_dir: Path) -> None:
    for filename in ("策划使用说明.md", "CHANGELOG.md"):
        source = base_dir / filename
        if source.exists():
            shutil.copy2(source, release_dir / filename)


def create_release_excel_dir(release_dir: Path) -> None:
    excel_dir = release_dir / "Excel"
    excel_dir.mkdir(parents=True, exist_ok=True)
    (excel_dir / "请把Excel配置表放到这里.txt").write_text(
        "请把需要导出的 .xlsx 配置表放到这个文件夹中。\n"
        "导表时请双击上一级目录中的 gen_data.bat。\n",
        encoding="utf-8",
    )


def write_build_info(base_dir: Path, release_dir: Path) -> None:
    payload = {
        "appName": APP_NAME,
        "version": APP_VERSION,
        "versionTag": get_version_tag(),
        "builtAt": datetime.now().isoformat(timespec="seconds"),
        "releaseDir": str(release_dir),
        "pythonExecutable": sys.executable,
        "entryPoint": str(base_dir / "main.py"),
    }
    (release_dir / "build-info.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    release_root = get_release_root(base_dir)
    release_dir = get_version_release_dir(base_dir)
    build_dir = get_build_artifacts_dir(base_dir)

    release_root.mkdir(parents=True, exist_ok=True)
    build_dir.mkdir(parents=True, exist_ok=True)

    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)

    exe_path = run_pyinstaller(base_dir, build_dir)
    shutil.copy2(exe_path, release_dir / exe_path.name)
    write_release_launcher(release_dir)
    copy_release_documents(base_dir, release_dir)
    create_release_excel_dir(release_dir)
    write_build_info(base_dir, release_dir)

    print("打包完成！")
    print(f"  - 版本号: {APP_VERSION}")
    print(f"  - 版本目录: {release_dir}")
    print(f"  - 可执行文件: {release_dir / exe_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
