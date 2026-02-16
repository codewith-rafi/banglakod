from __future__ import annotations

import argparse
from pathlib import Path
import sys

from interpreter import BanglaRuntimeError, Interpreter
from lexer import Lexer
from parser import Parser


def run_source(source: str) -> int:
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    if parser.errors:
        for err in parser.errors:
            print(f"Parser error: {err}")
        return 1
    interpreter = Interpreter()
    try:
        interpreter.evaluate(program)
    except BanglaRuntimeError as exc:
        print(f"Runtime error: {exc}")
        return 1
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Bangla based interpreter (.bn)")
    parser.add_argument("file", help="Path to .bn file")
    args = parser.parse_args(argv)

    path = Path(args.file)
    if path.suffix != ".bn":
        print("Shudhu .bn file chola jabe.")
        return 1
    if not path.exists():
        print("File paoa jay nai.")
        return 1
    return run_source(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))