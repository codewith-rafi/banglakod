# Banglakod

Banglakod is a small Bangla-flavored programming language written in Python. The syntax uses Bangla keywords spelled in English, aimed at beginner-friendly learning.

File extension: `.bn`

## Features

- Variables and assignment
- Print/output
- If/else
- While loops
- Functions (basic)
- Expressions with arithmetic and comparisons
- Booleans and logical operators

## Keywords

- dhoro = variable declaration
- lekho = print/output
- jodi = if
- nahole = else
- jokhon = while
- function = function
- ferot = return
- sotti = true
- mittha = false
- ar = and
- ba = or
- na = not

## Example

```bn
dhoro a = 10;
dhoro b = 2;

lekho a + b;

jodi a > b {
    lekho "a boro";
} nahole {
    lekho "b boro";
}

dhoro i = 0;
jokhon i < 3 {
    lekho i;
    i = i + 1;
}

function jog(x, y) {
    ferot x + y;
}

lekho jog(5, 7);
```

## Run

```bash
python main.py examples/hello.bn
```

## Installation

Python 3.10+ recommended.

Optional virtual environment:

```bash
python -m venv .venv
./.venv/Scripts/activate
```

Conda environment:

```bash
conda create -n banglakod python=3.12
conda activate banglakod
```

## Project Structure

- lexer.py: Tokenizer for Banglakod source
- parser.py: Pratt-style parser building the AST
- bangla_ast.py: AST node definitions
- bangla_token.py: Token definitions
- interpreter.py: Evaluator/runtime
- keywords.py: Bangla keyword table
- examples/: Sample .bn programs
- tests/: Basic tests

## Notes

- Statements accept optional semicolons.
- Assignment works with `name = expression`.
- Integers, strings, and booleans are supported.
- Error messages are shown in Bangla-style phrasing.

## Tests

```bash
pytest -q
```

## Limitations

- No floats yet (integers only).
- No arrays or dictionaries yet.
- No modules/import system yet.
