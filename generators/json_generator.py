from __future__ import annotations

import json
from pathlib import Path

from config import JSON_DIRNAME
from parser import SheetData


def generate_json_files(sheets: list[SheetData], output_dir: Path) -> None:
    json_dir = output_dir / JSON_DIRNAME
    json_dir.mkdir(parents=True, exist_ok=True)

    for sheet in sheets:
        payload = {"items": sheet.records}
        file_path = json_dir / f"{sheet.sheet_name}.json"
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
