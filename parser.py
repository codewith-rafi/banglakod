from __future__ import annotations

from enum import IntEnum
from typing import Callable, List, Optional

import bangla_ast
from lexer import Lexer
from bangla_token import Token, TokenType


class Precedence(IntEnum):
    LOWEST = 0
    OR = 1
    AND = 2
    EQUALS = 3
    LESSGREATER = 4
    SUM = 5
    PRODUCT = 6
    POWER = 7
    PREFIX = 8
    CALL = 9


PRECEDENCES = {
    TokenType.OR: Precedence.OR,
    TokenType.AND: Precedence.AND,
    TokenType.EQ: Precedence.EQUALS,
    TokenType.NEQ: Precedence.EQUALS,
    TokenType.LT: Precedence.LESSGREATER,
    TokenType.GT: Precedence.LESSGREATER,
    TokenType.LE: Precedence.LESSGREATER,
    TokenType.GE: Precedence.LESSGREATER,
    TokenType.PLUS: Precedence.SUM,
    TokenType.MINUS: Precedence.SUM,
    TokenType.ASTERISK: Precedence.PRODUCT,
    TokenType.SLASH: Precedence.PRODUCT,
    TokenType.MODULUS: Precedence.PRODUCT,
    TokenType.POW: Precedence.POWER,
    TokenType.LPAREN: Precedence.CALL,
}


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.errors: List[str] = []
        self.cur_token: Token = self.lexer.next_token()
        self.peek_token: Token = self.lexer.next_token()

        self.prefix_parse_fns: dict[TokenType, Callable[[], bangla_ast.Node]] = {
            TokenType.IDENT: self._parse_identifier,
            TokenType.INT: self._parse_integer_literal,
            TokenType.STRING: self._parse_string_literal,
            TokenType.TRUE: self._parse_boolean_literal,
            TokenType.FALSE: self._parse_boolean_literal,
            TokenType.MINUS: self._parse_prefix_expression,
            TokenType.PLUS: self._parse_prefix_expression,
            TokenType.NOT: self._parse_prefix_expression,
            TokenType.LPAREN: self._parse_grouped_expression,
        }

        self.infix_parse_fns: dict[TokenType, Callable[[bangla_ast.Node], bangla_ast.Node]] = {
            TokenType.PLUS: self._parse_infix_expression,
            TokenType.MINUS: self._parse_infix_expression,
            TokenType.ASTERISK: self._parse_infix_expression,
            TokenType.SLASH: self._parse_infix_expression,
            TokenType.MODULUS: self._parse_infix_expression,
            TokenType.POW: self._parse_infix_expression,
            TokenType.EQ: self._parse_infix_expression,
            TokenType.NEQ: self._parse_infix_expression,
            TokenType.LT: self._parse_infix_expression,
            TokenType.GT: self._parse_infix_expression,
            TokenType.LE: self._parse_infix_expression,
            TokenType.GE: self._parse_infix_expression,
            TokenType.AND: self._parse_infix_expression,
            TokenType.OR: self._parse_infix_expression,
            TokenType.LPAREN: self._parse_call_expression,
        }

    def _next_token(self) -> None:
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def _cur_token_is(self, token_type: TokenType) -> bool:
        return self.cur_token.type == token_type

    def _peek_token_is(self, token_type: TokenType) -> bool:
        return self.peek_token.type == token_type

    def _expect_peek(self, token_type: TokenType) -> bool:
        if self._peek_token_is(token_type):
            self._next_token()
            return True
        self._peek_error(token_type)
        return False

    def _peek_error(self, token_type: TokenType) -> None:
        message = (
            f"Line {self.peek_token.line}, Col {self.peek_token.column}: "
            f"peyar chilo {token_type.value}, kintu paoa gelo {self.peek_token.type.value}."
        )
        self.errors.append(message)

    def parse_program(self) -> bangla_ast.Program:
        statements: List[bangla_ast.Node] = []
        while self.cur_token.type != TokenType.EOF:
            stmt = self._parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self._next_token()
        return bangla_ast.Program(statements)

    def _parse_statement(self) -> Optional[bangla_ast.Node]:
        if self._cur_token_is(TokenType.IDENT) and self._peek_token_is(TokenType.ASSIGN):
            return self._parse_assign_stmt()
        match self.cur_token.type:
            case TokenType.DHORO:
                return self._parse_var_decl()
            case TokenType.LEKHO:
                return self._parse_print_stmt()
            case TokenType.JODI:
                return self._parse_if_stmt()
            case TokenType.JOKHON:
                return self._parse_while_stmt()
            case TokenType.FUNCTION:
                return self._parse_function_def()
            case TokenType.FEROT:
                return self._parse_return_stmt()
            case TokenType.LBRACE:
                return self._parse_block_statement()
            case _:
                return self._parse_expression_statement()

    def _parse_assign_stmt(self) -> Optional[bangla_ast.AssignStmt]:
        name = bangla_ast.Identifier(self.cur_token.literal, self.cur_token.line, self.cur_token.column)
        if not self._expect_peek(TokenType.ASSIGN):
            return None
        self._next_token()
        value = self._parse_expression(Precedence.LOWEST)
        if self._peek_token_is(TokenType.SEMICOLON):
            self._next_token()
        return bangla_ast.AssignStmt(name, value)

    def _parse_var_decl(self) -> Optional[bangla_ast.VarDecl]:
        if not self._expect_peek(TokenType.IDENT):
            return None
        name = bangla_ast.Identifier(self.cur_token.literal, self.cur_token.line, self.cur_token.column)
        if not self._expect_peek(TokenType.ASSIGN):
            return None
        self._next_token()
        value = self._parse_expression(Precedence.LOWEST)
        if self._peek_token_is(TokenType.SEMICOLON):
            self._next_token()
        return bangla_ast.VarDecl(name, value)

    def _parse_print_stmt(self) -> Optional[bangla_ast.PrintStmt]:
        self._next_token()
        expression = self._parse_expression(Precedence.LOWEST)
        if self._peek_token_is(TokenType.SEMICOLON):
            self._next_token()
        return bangla_ast.PrintStmt(expression)

    def _parse_return_stmt(self) -> Optional[bangla_ast.ReturnStmt]:
        if self._peek_token_is(TokenType.SEMICOLON) or self._peek_token_is(TokenType.RBRACE):
            if self._peek_token_is(TokenType.SEMICOLON):
                self._next_token()
            return bangla_ast.ReturnStmt(None)
        self._next_token()
        value = self._parse_expression(Precedence.LOWEST)
        if self._peek_token_is(TokenType.SEMICOLON):
            self._next_token()
        return bangla_ast.ReturnStmt(value)

    def _parse_if_stmt(self) -> Optional[bangla_ast.IfStmt]:
        self._next_token()
        condition = self._parse_expression(Precedence.LOWEST)
        if not self._expect_peek(TokenType.LBRACE):
            return None
        consequence = self._parse_block_statement()
        alternative = None
        if self._peek_token_is(TokenType.NAHOLE):
            self._next_token()
            if not self._expect_peek(TokenType.LBRACE):
                return None
            alternative = self._parse_block_statement()
        return bangla_ast.IfStmt(condition, consequence, alternative)

    def _parse_while_stmt(self) -> Optional[bangla_ast.WhileStmt]:
        self._next_token()
        condition = self._parse_expression(Precedence.LOWEST)
        if not self._expect_peek(TokenType.LBRACE):
            return None
        body = self._parse_block_statement()
        return bangla_ast.WhileStmt(condition, body)

    def _parse_function_def(self) -> Optional[bangla_ast.FunctionDef]:
        if not self._expect_peek(TokenType.IDENT):
            return None
        name = bangla_ast.Identifier(self.cur_token.literal, self.cur_token.line, self.cur_token.column)
        if not self._expect_peek(TokenType.LPAREN):
            return None
        params = self._parse_function_params()
        if not self._expect_peek(TokenType.LBRACE):
            return None
        body = self._parse_block_statement()
        return bangla_ast.FunctionDef(name, params, body)

    def _parse_function_params(self) -> List[bangla_ast.Identifier]:
        params: List[bangla_ast.Identifier] = []
        if self._peek_token_is(TokenType.RPAREN):
            self._next_token()
            return params
        self._next_token()
        params.append(bangla_ast.Identifier(self.cur_token.literal, self.cur_token.line, self.cur_token.column))
        while self._peek_token_is(TokenType.COMMA):
            self._next_token()
            self._next_token()
            params.append(bangla_ast.Identifier(self.cur_token.literal, self.cur_token.line, self.cur_token.column))
        if not self._expect_peek(TokenType.RPAREN):
            return []
        return params

    def _parse_block_statement(self) -> bangla_ast.Block:
        statements: List[bangla_ast.Node] = []
        self._next_token()
        while not self._cur_token_is(TokenType.RBRACE) and not self._cur_token_is(TokenType.EOF):
            stmt = self._parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self._next_token()
        return bangla_ast.Block(statements)

    def _parse_expression_statement(self) -> Optional[bangla_ast.ExprStmt]:
        expression = self._parse_expression(Precedence.LOWEST)
        if self._peek_token_is(TokenType.SEMICOLON):
            self._next_token()
        if expression is None:
            return None
        return bangla_ast.ExprStmt(expression)

    def _parse_expression(self, precedence: Precedence) -> Optional[bangla_ast.Node]:
        prefix = self.prefix_parse_fns.get(self.cur_token.type)
        if prefix is None:
            self.errors.append(
                f"Line {self.cur_token.line}, Col {self.cur_token.column}: "
                f"expression start korar jonno thik token pai nai ({self.cur_token.type.value})."
            )
            return None
        left_expr = prefix()

        while not self._peek_token_is(TokenType.SEMICOLON) and precedence < self._peek_precedence():
            infix = self.infix_parse_fns.get(self.peek_token.type)
            if infix is None:
                return left_expr
            self._next_token()
            left_expr = infix(left_expr)
        return left_expr

    def _parse_identifier(self) -> bangla_ast.Identifier:
        return bangla_ast.Identifier(self.cur_token.literal, self.cur_token.line, self.cur_token.column)

    def _parse_integer_literal(self) -> bangla_ast.IntegerLiteral:
        return bangla_ast.IntegerLiteral(int(self.cur_token.literal), self.cur_token.line, self.cur_token.column)

    def _parse_string_literal(self) -> bangla_ast.StringLiteral:
        return bangla_ast.StringLiteral(self.cur_token.literal, self.cur_token.line, self.cur_token.column)

    def _parse_boolean_literal(self) -> bangla_ast.BooleanLiteral:
        return bangla_ast.BooleanLiteral(
            self.cur_token.type == TokenType.TRUE,
            self.cur_token.line,
            self.cur_token.column,
        )

    def _parse_grouped_expression(self) -> Optional[bangla_ast.Node]:
        self._next_token()
        expression = self._parse_expression(Precedence.LOWEST)
        if not self._expect_peek(TokenType.RPAREN):
            return None
        return expression

    def _parse_prefix_expression(self) -> bangla_ast.PrefixExpr:
        operator = self.cur_token.literal
        self._next_token()
        right = self._parse_expression(Precedence.PREFIX)
        return bangla_ast.PrefixExpr(operator, right)

    def _parse_infix_expression(self, left: bangla_ast.Node) -> bangla_ast.InfixExpr:
        operator = self.cur_token.literal
        precedence = self._cur_precedence()
        if self.cur_token.type == TokenType.POW:
            precedence = Precedence.POWER - 1
        self._next_token()
        right = self._parse_expression(precedence)
        return bangla_ast.InfixExpr(left, operator, right)

    def _parse_call_expression(self, function: bangla_ast.Node) -> bangla_ast.CallExpr:
        args = self._parse_expression_list(TokenType.RPAREN)
        return bangla_ast.CallExpr(function, args)

    def _parse_expression_list(self, end: TokenType) -> List[bangla_ast.Node]:
        args: List[bangla_ast.Node] = []
        if self._peek_token_is(end):
            self._next_token()
            return args
        self._next_token()
        args.append(self._parse_expression(Precedence.LOWEST))
        while self._peek_token_is(TokenType.COMMA):
            self._next_token()
            self._next_token()
            args.append(self._parse_expression(Precedence.LOWEST))
        if not self._expect_peek(end):
            return []
        return args

    def _peek_precedence(self) -> Precedence:
        return PRECEDENCES.get(self.peek_token.type, Precedence.LOWEST)

    def _cur_precedence(self) -> Precedence:
        return PRECEDENCES.get(self.cur_token.type, Precedence.LOWEST)
