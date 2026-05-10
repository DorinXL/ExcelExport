from __future__ import annotations

import argparse
import sys
from pathlib import Path

from config import DEFAULT_EXCEL_DIR, DEFAULT_OUTPUT_DIR
from generators import (
    generate_cs_files,
    generate_enum,
    generate_json_files,
    generate_manifest,
)
from logger import Logger
from parser import parse_excel_file
from scanner import scan_excel_files
from utils import (
    clean_output_directory,
    deduplicate_sheets_by_name,
    ensure_output_structure,
    resolve_base_directory,
    resolve_work_path,
)
from validator import validate_all


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unity Excel 导表工具")
    parser.add_argument(
        "--excel-dir",
        default=str(DEFAULT_EXCEL_DIR),
        help="Excel 输入目录，默认相对程序目录为 ./Excel/",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="输出目录，默认相对程序目录为 ./Output/",
    )
    return parser


def main() -> int:
    args = build_argument_parser().parse_args()
    base_dir = resolve_base_directory()
    excel_dir = resolve_work_path(args.excel_dir, base_dir)
    output_dir = resolve_work_path(args.output_dir, base_dir)

    logger = Logger()

    try:
        excel_files = scan_excel_files(excel_dir)
    except FileNotFoundError as exc:
        print(f"[错误] {exc}")
        return 1

    if not excel_files:
        print(f"[错误] 未在 {excel_dir} 目录下找到 Excel 文件")
        return 1

    all_sheets = []
    for filepath in excel_files:
        sheets, errors = parse_excel_file(filepath)
        all_sheets.extend(sheets)
        logger.extend_errors(errors)

    if not all_sheets:
        logger.add_error("未找到有效 Sheet")

    logger.extend_errors(validate_all(all_sheets))

    if logger.has_errors():
        clean_output_directory(output_dir)
        logger.print_summary()
        return 1

    output_sheets = deduplicate_sheets_by_name(all_sheets)
    clean_output_directory(output_dir)
    ensure_output_structure(output_dir)
    generate_json_files(output_sheets, output_dir)
    generate_cs_files(output_sheets, output_dir)
    generate_manifest(output_sheets, output_dir)
    generate_enum(output_sheets, output_dir)

    print("导表完成！")
    print(f"  - 共处理 {len(excel_files)} 个 Excel 文件")
    print(f"  - 共解析 {len(all_sheets)} 个有效 Sheet")
    print(f"  - 共生成 {len(output_sheets)} 张配置表")
    print(f"  - 输出目录: {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
