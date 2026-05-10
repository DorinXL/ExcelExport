from __future__ import annotations

from typing import Iterable


class Logger:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def extend_errors(self, messages: Iterable[str]) -> None:
        self.errors.extend(messages)

    def has_errors(self) -> bool:
        return bool(self.errors)

    def print_summary(self) -> None:
        if not self.errors:
            print("导表成功！")
            return

        print(f"导表失败，共发现 {len(self.errors)} 个错误：")
        for error in self.errors:
            print(f"[错误] {error}")
