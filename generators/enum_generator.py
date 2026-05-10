from __future__ import annotations

from pathlib import Path

from parser import SheetData

FILE_HEADER = "// 本文件由导表工具自动生成，请勿手动修改"


def generate_enum(sheets: list[SheetData], output_dir: Path) -> None:
    members = [f"    {sheet.sheet_name}," for sheet in sheets]
    content = "\n".join([FILE_HEADER, "public enum ConfigTable", "{", *members, "}", ""])
    file_path = output_dir / "ConfigTables.cs"
    file_path.write_text(content, encoding="utf-8")
