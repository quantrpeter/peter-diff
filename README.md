# peter-diff

A simple Python CLI tool to compare two text files and output their differences, similar to the Unix `diff` command.

## Installation

```bash
pip install -e .
pip uninstall peter-diff
```
OR

```sh
pip install peter-diff
```

## Usage

```sh
pydiff file1.txt file2.txt
```

## Publishing to PyPI

```
pip install build twine
python -m build
twine upload dist/*
```

When prompted, use `__token__` as the username and your PyPI API token as the password.

To skip the prompt, create a `~/.pypirc` file:

```ini
[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE
```

> **Note:** Bump the `version` in `pyproject.toml` before each upload — PyPI rejects duplicate version numbers.

## Requirements

- Python >= 3.9
- No external dependencies

## License

MIT
