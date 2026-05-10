from __future__ import annotations

from parser import SheetData


def validate_all(sheets: list[SheetData]) -> list[str]:
    errors: list[str] = []
    for sheet in sheets:
        errors.extend(validate_sheet(sheet))
    return errors


def validate_sheet(sheet: SheetData) -> list[str]:
    errors: list[str] = []
    errors.extend(check_id_field(sheet.headers, sheet.types, sheet.file_name, sheet.sheet_name))
    errors.extend(check_duplicate_ids(sheet.records, sheet.file_name, sheet.sheet_name))
    return errors


def check_id_field(
    headers: list[str], types: list[str], file_name: str, sheet_name: str
) -> list[str]:
    if "id" not in headers:
        return [f"{file_name} - Sheet '{sheet_name}'：缺少必填主键字段 'id'"]

    id_index = headers.index("id")
    if types[id_index] != "int":
        return [
            f"{file_name} - Sheet '{sheet_name}'：主键字段 'id' 类型必须为 'int'，当前为 '{types[id_index]}'"
        ]

    return []


def check_duplicate_ids(records: list[dict[str, object]], file_name: str, sheet_name: str) -> list[str]:
    errors: list[str] = []
    seen: set[int] = set()

    for record in records:
        id_value = record.get("id")
        if not isinstance(id_value, int):
            continue
        if id_value in seen:
            errors.append(f"{file_name} - Sheet '{sheet_name}'：id 值 {id_value} 重复出现")
        else:
            seen.add(id_value)

    return errors
