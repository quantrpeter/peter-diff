# peter-diff

A Python CLI tool for side-by-side diffing of files and folders.

!()[image/2026-05-23T01_18_19.png]

## Installation

```bash
pip install -e .
```
OR

```sh
pip install peter-diff
```

## Usage

### Compare two files

```sh
peter-diff file1.txt file2.txt
```

Displays a side-by-side diff with line numbers. Changed characters within a line are highlighted. Identical files print `same`.

!()[image/file.png]

### Compare two folders

```sh
peter-diff dir1/ dir2/
```

Displays a side-by-side tree view of both directories:

```
dir1/                          │ dir2/
───────────────────────────────┼───────────────────────────────
├── config.txt                 │ ├── config.txt
├── hello.py         diff      │ ├── hello.py
├── only_in_1.txt    ←         │
                    →          │ ├── only_in_2.txt
└── src/                       │ └── src/
    └── main.py      diff      │     └── main.py
```

Status indicators:
| Symbol | Meaning |
|--------|---------|
| *(none)* | identical |
| `diff` | file differs |
| `←` | only in left folder |
| `→` | only in right folder |
| `bin` | binary / unreadable, skipped |

!()[image/folder.png]

### Flags

| Flag | Description |
|------|-------------|
| `-o` | Only show differences — hide identical files/lines |

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
