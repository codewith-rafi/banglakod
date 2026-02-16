from __future__ import annotations

from bangla_token import TokenType

KEYWORDS = {
    "dhoro": TokenType.DHORO,
    "lekho": TokenType.LEKHO,
    "jodi": TokenType.JODI,
    "nahole": TokenType.NAHOLE,
    "jokhon": TokenType.JOKHON,
    "function": TokenType.FUNCTION,
    "ferot": TokenType.FEROT,
    "sotti": TokenType.TRUE,
    "mittha": TokenType.FALSE,
    "ar": TokenType.AND,
    "ba": TokenType.OR,
    "na": TokenType.NOT,
}


def lookup_ident(literal: str) -> TokenType:
    return KEYWORDS.get(literal, TokenType.IDENT)
