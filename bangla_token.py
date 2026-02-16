from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class TokenType(Enum):
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"

    IDENT = "IDENT"
    INT = "INT"
    STRING = "STRING"
    TRUE = "TRUE"
    FALSE = "FALSE"

    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    ASTERISK = "*"
    SLASH = "/"
    MODULUS = "%"
    POW = "**"

    LT = "<"
    GT = ">"
    LE = "<="
    GE = ">="
    EQ = "=="
    NEQ = "!="

    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    DHORO = "DHORO"
    LEKHO = "LEKHO"
    JODI = "JODI"
    NAHOLE = "NAHOLE"
    JOKHON = "JOKHON"
    FUNCTION = "FUNCTION"
    FEROT = "FEROT"


@dataclass(frozen=True)
class Token:
    type: TokenType
    literal: Any
    line: int
    column: int