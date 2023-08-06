print-python
============

[Print](https://github.com/gduverger/print) Python client

## Installation

```bash
$ pipenv install print-python
```

## Usage

```python
>>> import print as prt
>>> prt = prt.Client(host='<host>', path='<path>', token='<token>')
>>> prt.post('As easy as rolling off a log')
```

## Test

```bash
# DOC https://docs.pytest.org/en/latest/usage.html#calling-pytest-through-python-m-pytest
python -m pytest
```
