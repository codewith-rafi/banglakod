# Banglakod

Banglakod is a small Bangla-flavored programming language written in Python. The syntax uses Bangla keywords spelled in English, aimed at beginner-friendly learning.

**Status**: Educational project | **Python**: 3.10+ | **License**: MIT

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

## Roadmap

- [ ] Float literals
- [ ] Arrays/lists
- [ ] Built-in functions (len, type, input)
- [ ] String concatenation
- [ ] For loops
- [ ] Comments (# support — already in lexer)
- [ ] File I/O

## Contributing

Contributions welcome! Feel free to open an issue or PR for:
- Bug fixes
- New language features
- Better error messages
- Documentation improvements

## License

MIT License. See LICENSE file for details.

## Authors

Built as an educational interpreter for learning language design and implementation.

## See Also

- [craftinginterpreters.com](https://craftinginterpreters.com) — Language interpreter design
- [Pratt parsing](https://en.wikipedia.org/wiki/Operator-precedence_parser) — Parser technique used
