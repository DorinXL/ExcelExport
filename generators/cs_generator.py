from __future__ import annotations

from pathlib import Path

from config import SCRIPTS_DIRNAME, TYPE_MAP
from parser import SheetData

FILE_HEADER = "// 本文件由导表工具自动生成，请勿手动修改"


def generate_cs_files(sheets: list[SheetData], output_dir: Path) -> None:
    scripts_dir = output_dir / SCRIPTS_DIRNAME
    scripts_dir.mkdir(parents=True, exist_ok=True)

    for sheet in sheets:
        field_lines = []
        for header, type_mark in zip(sheet.headers, sheet.types):
            cs_type = TYPE_MAP[type_mark]
            field_lines.append(f"    public {cs_type} {header};")

        content = "\n".join(
            [
                FILE_HEADER,
                "[System.Serializable]",
                f"public class {sheet.sheet_name}Config",
                "{",
                *field_lines,
                "}",
                "",
            ]
        )
        file_path = scripts_dir / f"{sheet.sheet_name}Config.cs"
        file_path.write_text(content, encoding="utf-8")
