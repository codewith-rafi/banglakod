from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

import bangla_ast


class BanglaRuntimeError(Exception):
    pass


class ReturnSignal(Exception):
    def __init__(self, value: Any) -> None:
        self.value = value


@dataclass
class Function:
    name: str
    params: List[str]
    body: bangla_ast.Block
    env: "Environment"


class Environment:
    def __init__(self, outer: Optional["Environment"] = None) -> None:
        self.store: dict[str, Any] = {}
        self.outer = outer

    def get(self, name: str) -> Any:
        if name in self.store:
            return self.store[name]
        if self.outer is not None:
            return self.outer.get(name)
        raise BanglaRuntimeError(f"Chena jai na: '{name}' variable nai.")

    def set(self, name: str, value: Any) -> None:
        self.store[name] = value

    def assign(self, name: str, value: Any, line: int | None = None, column: int | None = None) -> None:
        if name in self.store:
            self.store[name] = value
            return
        if self.outer is not None:
            self.outer.assign(name, value, line, column)
            return
        if line is not None and column is not None:
            raise BanglaRuntimeError(
                f"Line {line}, Col {column}: Chena jai na: '{name}' variable nai."
            )
        raise BanglaRuntimeError(f"Chena jai na: '{name}' variable nai.")


class Interpreter:
    def __init__(self) -> None:
        self.global_env = Environment()

    def evaluate(self, node: bangla_ast.Node) -> Any:
        if isinstance(node, bangla_ast.Program):
            return self._eval_program(node)
        if isinstance(node, bangla_ast.Block):
            return self._eval_block(node, Environment(self.global_env))
        if isinstance(node, bangla_ast.VarDecl):
            value = self.evaluate(node.value)
            self.global_env.set(node.name.name, value)
            return value
        if isinstance(node, bangla_ast.AssignStmt):
            value = self.evaluate(node.value)
            self.global_env.assign(node.name.name, value, node.name.line, node.name.column)
            return value
        if isinstance(node, bangla_ast.PrintStmt):
            value = self.evaluate(node.expression)
            print(self._stringify(value))
            return value
        if isinstance(node, bangla_ast.ExprStmt):
            return self.evaluate(node.expression)
        if isinstance(node, bangla_ast.IfStmt):
            return self._eval_if(node)
        if isinstance(node, bangla_ast.WhileStmt):
            return self._eval_while(node)
        if isinstance(node, bangla_ast.FunctionDef):
            function = Function(node.name.name, [p.name for p in node.params], node.body, self.global_env)
            self.global_env.set(node.name.name, function)
            return function
        if isinstance(node, bangla_ast.ReturnStmt):
            value = self.evaluate(node.value) if node.value is not None else None
            raise ReturnSignal(value)
        if isinstance(node, bangla_ast.Identifier):
            try:
                return self.global_env.get(node.name)
            except BanglaRuntimeError as exc:
                if node.line and node.column:
                    raise BanglaRuntimeError(
                        f"Line {node.line}, Col {node.column}: {exc}"
                    ) from exc
                raise
        if isinstance(node, bangla_ast.IntegerLiteral):
            return node.value
        if isinstance(node, bangla_ast.StringLiteral):
            return node.value
        if isinstance(node, bangla_ast.BooleanLiteral):
            return node.value
        if isinstance(node, bangla_ast.PrefixExpr):
            right = self.evaluate(node.right)
            return self._eval_prefix(node.operator, right)
        if isinstance(node, bangla_ast.InfixExpr):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            return self._eval_infix(node.operator, left, right)
        if isinstance(node, bangla_ast.CallExpr):
            function = self.evaluate(node.function)
            args = [self.evaluate(arg) for arg in node.args]
            return self._apply_function(function, args)
        raise BanglaRuntimeError("Bujhte parchi na emon ekta expression.")

    def _eval_program(self, program: bangla_ast.Program) -> Any:
        result = None
        for stmt in program.statements:
            result = self.evaluate(stmt)
        return result

    def _eval_block(self, block: bangla_ast.Block, env: Environment) -> Any:
        result = None
        previous_env = self.global_env
        self.global_env = env
        try:
            for stmt in block.statements:
                result = self.evaluate(stmt)
        finally:
            self.global_env = previous_env
        return result

    def _eval_if(self, stmt: bangla_ast.IfStmt) -> Any:
        condition = self.evaluate(stmt.condition)
        if self._is_truthy(condition):
            return self._eval_block(stmt.consequence, Environment(self.global_env))
        if stmt.alternative is not None:
            return self._eval_block(stmt.alternative, Environment(self.global_env))
        return None

    def _eval_while(self, stmt: bangla_ast.WhileStmt) -> Any:
        result = None
        loop_env = Environment(self.global_env)
        while self._is_truthy(self.evaluate(stmt.condition)):
            result = self._eval_block(stmt.body, loop_env)
        return result

    def _apply_function(self, function: Any, args: List[Any]) -> Any:
        if not isinstance(function, Function):
            raise BanglaRuntimeError("Function na emon kisu call kora jacche na.")
        if len(args) != len(function.params):
            raise BanglaRuntimeError("Argument shonkha milche na.")
        env = Environment(function.env)
        for name, value in zip(function.params, args):
            env.set(name, value)
        try:
            return self._eval_block(function.body, env)
        except ReturnSignal as signal:
            return signal.value

    def _eval_prefix(self, operator: str, right: Any) -> Any:
        if operator == "-":
            return -self._ensure_number(right)
        if operator == "+":
            return self._ensure_number(right)
        if operator == "na":
            return not self._is_truthy(right)
        raise BanglaRuntimeError(f"Ojoggo prefix operator '{operator}'.")

    def _eval_infix(self, operator: str, left: Any, right: Any) -> Any:
        if operator in {"+", "-", "*", "/", "%", "**"}:
            return self._eval_math(operator, left, right)
        if operator in {"<", ">", "<=", ">=", "==", "!="}:
            return self._eval_compare(operator, left, right)
        if operator == "ar":
            return self._is_truthy(left) and self._is_truthy(right)
        if operator == "ba":
            return self._is_truthy(left) or self._is_truthy(right)
        raise BanglaRuntimeError(f"Ojoggo operator '{operator}'.")

    def _eval_math(self, operator: str, left: Any, right: Any) -> Any:
        left_num = self._ensure_number(left)
        right_num = self._ensure_number(right)
        if operator == "+":
            return left_num + right_num
        if operator == "-":
            return left_num - right_num
        if operator == "*":
            return left_num * right_num
        if operator == "/":
            if right_num == 0:
                raise BanglaRuntimeError("Bhag kora jabe na: 0 diye vag.")
            return left_num // right_num
        if operator == "%":
            return left_num % right_num
        if operator == "**":
            return left_num**right_num
        raise BanglaRuntimeError("Ojoggo math operator.")

    def _eval_compare(self, operator: str, left: Any, right: Any) -> bool:
        if operator == "==":
            return left == right
        if operator == "!=":
            return left != right
        left_num = self._ensure_number(left)
        right_num = self._ensure_number(right)
        if operator == "<":
            return left_num < right_num
        if operator == ">":
            return left_num > right_num
        if operator == "<=":
            return left_num <= right_num
        if operator == ">=":
            return left_num >= right_num
        raise BanglaRuntimeError("Ojoggo tulona operator.")

    def _ensure_number(self, value: Any) -> int:
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, int):
            return value
        raise BanglaRuntimeError("Number dorkar chilo.")

    def _is_truthy(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        return True

    def _stringify(self, value: Any) -> str:
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "sotti" if value else "mittha"
        return str(value)
