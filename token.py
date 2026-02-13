from enum import Enum
from typing import Any

class TokenType(Enum):
    # Special Tokens
    EOF = 'EOF'
    ILLEGAL = 'ILLEGAL'

    # Data Types
    INT = 'INT'
    FLOAT = 'FLOAT'

    # Arithmetic Operatores
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    ASTERISK = 'ASTERISK'
    SLASH = 'SLASH'
    MODULUS = 'MODULUS'
    POW = 'POW'

    # Symbols
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'

    class Token:
        def __init__(self, type: TokenType, literal: Any, line_no: int, position: int) -> None:
            self.type = type
            self.literal = literal
            self.line_no = line_no
            self.position = position
        
        def __str__(self) -> str:
            return f'Token[type={self.type}, literal={self.literal}, line_no={self.line_no}, position={self.position}]'
        
        def __repr__(self) -> str:
            return str(self)