from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Sequence

from config import JSON_DIRNAME, SCRIPTS_DIRNAME

if TYPE_CHECKING:
    from parser import SheetData


def is_blank(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def normalize_text(value: object) -> str:
    if value is None:
        return ""
    return str(value)


def is_blank_row(values: Sequence[object]) -> bool:
    return all(is_blank(value) for value in values)


def trim_trailing_empty_columns(
    comments: list[str], headers: list[str], types: list[str], default_values: list[str]
) -> tuple[list[str], list[str], list[str], list[str]]:
    while (
        headers
        and comments[-1].strip() == ""
        and headers[-1].strip() == ""
        and types[-1].strip() == ""
        and default_values[-1].strip() == ""
    ):
        comments.pop()
        headers.pop()
        types.pop()
        default_values.pop()
    return comments, headers, types, default_values


def clean_output_directory(output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


def ensure_output_structure(output_dir: Path) -> None:
    (output_dir / JSON_DIRNAME).mkdir(parents=True, exist_ok=True)
    (output_dir / SCRIPTS_DIRNAME).mkdir(parents=True, exist_ok=True)


def resolve_base_directory() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def resolve_work_path(raw_path: str, base_dir: Path) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def deduplicate_sheets_by_name(sheets: Iterable["SheetData"]) -> list["SheetData"]:
    latest_by_name: dict[str, "SheetData"] = {}
    for sheet in sheets:
        if sheet.sheet_name in latest_by_name:
            del latest_by_name[sheet.sheet_name]
        latest_by_name[sheet.sheet_name] = sheet
    return list(latest_by_name.values())
