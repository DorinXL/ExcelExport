from pathlib import Path

# 默认输入/输出目录。实际运行时会基于脚本或 exe 所在目录解析。
DEFAULT_EXCEL_DIR = Path("Excel")
DEFAULT_OUTPUT_DIR = Path("Output")
JSON_DIRNAME = "Json"
SCRIPTS_DIRNAME = "Scripts"

SKIP_SHEET_PREFIXES = ("#", "_")
SKIP_FILE_PREFIXES = ("~",)
EXCEL_EXTENSION = ".xlsx"

TITLE_ROW_INDEX = 0
TYPE_ROW_INDEX = 1
DEFAULT_VALUE_ROW_INDEX = 2
HEADER_ROW_INDEX = 3
COMMENT_ROW_INDEX = 4
DATA_START_ROW_INDEX = 5

ARRAY_SEPARATOR = "|"
ID_FIELD_NAME = "id"
ID_FIELD_TYPE = "int"

# type_mark -> C# type
TYPE_MAP = {
    "int": "int",
    "float": "float",
    "string": "string",
    "bool": "bool",
    "array_int": "int[]",
    "array_float": "float[]",
    "array_string": "string[]",
}
