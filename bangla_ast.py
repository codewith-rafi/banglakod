from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


class Node:
    pass


@dataclass
class Program(Node):
    statements: List[Node]


@dataclass
class Block(Node):
    statements: List[Node]


@dataclass
class VarDecl(Node):
    name: "Identifier"
    value: Node


@dataclass
class AssignStmt(Node):
    name: "Identifier"
    value: Node


@dataclass
class PrintStmt(Node):
    expression: Node


@dataclass
class ExprStmt(Node):
    expression: Node


@dataclass
class IfStmt(Node):
    condition: Node
    consequence: Block
    alternative: Optional[Block]


@dataclass
class WhileStmt(Node):
    condition: Node
    body: Block


@dataclass
class FunctionDef(Node):
    name: "Identifier"
    params: List["Identifier"]
    body: Block


@dataclass
class ReturnStmt(Node):
    value: Optional[Node]


@dataclass
class Identifier(Node):
    name: str
    line: int = 0
    column: int = 0


@dataclass
class IntegerLiteral(Node):
    value: int
    line: int = 0
    column: int = 0


@dataclass
class StringLiteral(Node):
    value: str
    line: int = 0
    column: int = 0


@dataclass
class BooleanLiteral(Node):
    value: bool
    line: int = 0
    column: int = 0


@dataclass
class PrefixExpr(Node):
    operator: str
    right: Node


@dataclass
class InfixExpr(Node):
    left: Node
    operator: str
    right: Node


@dataclass
class CallExpr(Node):
    function: Node
    args: List[Node]
