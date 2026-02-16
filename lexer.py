from __future__ import annotations

from keywords import lookup_ident
from bangla_token import Token, TokenType


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.position = 0
        self.read_position = 0
        self.line = 1
        self.column = 0
        self.current_char: str | None = None
        self._read_char()

    def _read_char(self) -> None:
        if self.read_position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.read_position]
        self.position = self.read_position
        self.read_position += 1
        if self.current_char == "\n":
            self.line += 1
            self.column = 0
        else:
            self.column += 1

    def _peek_char(self) -> str | None:
        if self.read_position >= len(self.source):
            return None
        return self.source[self.read_position]

    def _skip_whitespace(self) -> None:
        while self.current_char is not None and self.current_char in " \t\r\n":
            self._read_char()

    def _skip_comment(self) -> None:
        while self.current_char is not None and self.current_char != "\n":
            self._read_char()

    def _read_identifier(self) -> str:
        start = self.position
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            self._read_char()
        return self.source[start:self.position]

    def _read_number(self) -> str:
        start = self.position
        while self.current_char is not None and self.current_char.isdigit():
            self._read_char()
        return self.source[start:self.position]

    def _read_string(self) -> str:
        self._read_char()
        start = self.position
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == "\\" and self._peek_char() == '"':
                self._read_char()
            self._read_char()
        literal = self.source[start:self.position]
        self._read_char()
        return literal

    def _make_token(self, token_type: TokenType, literal: str) -> Token:
        return Token(token_type, literal, self.line, self.column)

    def next_token(self) -> Token:
        self._skip_whitespace()

        if self.current_char == "#":
            self._skip_comment()
            self._skip_whitespace()

        if self.current_char is None:
            return self._make_token(TokenType.EOF, "")

        match self.current_char:
            case "=":
                if self._peek_char() == "=":
                    self._read_char()
                    tok = self._make_token(TokenType.EQ, "==")
                else:
                    tok = self._make_token(TokenType.ASSIGN, "=")
            case "+":
                tok = self._make_token(TokenType.PLUS, "+")
            case "-":
                tok = self._make_token(TokenType.MINUS, "-")
            case "*":
                if self._peek_char() == "*":
                    self._read_char()
                    tok = self._make_token(TokenType.POW, "**")
                else:
                    tok = self._make_token(TokenType.ASTERISK, "*")
            case "/":
                tok = self._make_token(TokenType.SLASH, "/")
            case "%":
                tok = self._make_token(TokenType.MODULUS, "%")
            case "<":
                if self._peek_char() == "=":
                    self._read_char()
                    tok = self._make_token(TokenType.LE, "<=")
                else:
                    tok = self._make_token(TokenType.LT, "<")
            case ">":
                if self._peek_char() == "=":
                    self._read_char()
                    tok = self._make_token(TokenType.GE, ">=")
                else:
                    tok = self._make_token(TokenType.GT, ">")
            case "!":
                if self._peek_char() == "=":
                    self._read_char()
                    tok = self._make_token(TokenType.NEQ, "!=")
                else:
                    tok = self._make_token(TokenType.ILLEGAL, "!")
            case ",":
                tok = self._make_token(TokenType.COMMA, ",")
            case ";":
                tok = self._make_token(TokenType.SEMICOLON, ";")
            case "(":
                tok = self._make_token(TokenType.LPAREN, "(")
            case ")":
                tok = self._make_token(TokenType.RPAREN, ")")
            case "{":
                tok = self._make_token(TokenType.LBRACE, "{")
            case "}":
                tok = self._make_token(TokenType.RBRACE, "}")
            case '"':
                literal = self._read_string()
                return self._make_token(TokenType.STRING, literal)
            case _:
                if self.current_char.isalpha() or self.current_char == "_":
                    literal = self._read_identifier()
                    token_type = lookup_ident(literal)
                    return self._make_token(token_type, literal)
                if self.current_char.isdigit():
                    literal = self._read_number()
                    return self._make_token(TokenType.INT, literal)
                tok = self._make_token(TokenType.ILLEGAL, self.current_char)

        self._read_char()
        return tok