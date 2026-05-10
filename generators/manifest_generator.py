from __future__ import annotations

import json
from pathlib import Path

from parser import SheetData


def generate_manifest(sheets: list[SheetData], output_dir: Path) -> None:
    manifest = {
        "tables": [
            {
                "sheetName": sheet.sheet_name,
                "excelFile": sheet.file_name,
                "jsonFile": f"{sheet.sheet_name}.json",
                "className": f"{sheet.sheet_name}Config",
                "idType": "int",
            }
            for sheet in sheets
        ]
    }

    file_path = output_dir / "manifest.json"
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(manifest, file, ensure_ascii=False, indent=2)
