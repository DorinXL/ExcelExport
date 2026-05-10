from __future__ import annotations

from pathlib import Path

from config import EXCEL_EXTENSION, SKIP_FILE_PREFIXES


def scan_excel_files(directory: Path) -> list[Path]:
    if not directory.exists():
        raise FileNotFoundError(f"Excel 目录不存在: {directory}")

    if not directory.is_dir():
        raise FileNotFoundError(f"Excel 目录不存在: {directory}")

    files = [
        path
        for path in directory.rglob(f"*{EXCEL_EXTENSION}")
        if path.is_file() and not path.name.startswith(SKIP_FILE_PREFIXES)
    ]
    return sorted(files, key=lambda path: str(path).lower())
