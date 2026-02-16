from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def run_source(source: str):
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert parser.errors == []
    interpreter = Interpreter()
    return interpreter.evaluate(program)


def test_boolean_and_logic():
    result = run_source("""
    dhoro a = sotti;
    dhoro b = mittha;
    lekho na b;
    lekho a ar b;
    lekho a ba b;
    """)
    assert result is True


def test_while_scope_persists():
    result = run_source("""
    dhoro i = 0;
    jokhon i < 3 {
        i = i + 1;
    }
    i;
    """)
    assert result == 3
