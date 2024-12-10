# PyInitials, because GvR is shorter than Guido van Rossum

```python
from pyinitials import initials

print(initials('Guido van Rossum')) # prints "GvR"
```

[![main](https://github.com/robvanderleek/pyinitials/actions/workflows/main.yml/badge.svg)](https://github.com/robvanderleek/pyinitials/actions/workflows/main.yml)

This project is a Python clone of the [JavaScript initials package](https://github.com/gr2m/initials).

# Installation

Install from [PyPi](https://pypi.org/project/pyinitials/), for example with
Poetry:

```shell
poetry add pyinitials
```


# Usage

```python
from pyinitials import initials, find, parse, add_to

initials('John Doe') # 'JD'

initials(['John Doe', 'Robert Roe']) # ['JD', 'RR']

# alias for initials('John Doe')
find('John Doe') # 'JD'

parse('John Doe') # Parts(name='John Doe', initials='JD', email=None)

# add initials to name(s)
add_to('John Doe') # 'John Doe (JD)'

# Pass existing initials for names
initials(['John Doe', 'Jane Dane'], existing={'John Doe': 'JD'}) # ['JD', 'JDa']
```

## Notes

Preffered initials can be passed in `(JD)`, e.g.

```python
initials('John Doe (JoDo)') # 'JoDo'
```

If a name contains an email, it gets ignored when calculating initials

```python
initials('John Doe joe@example.com') # 'JD'
```

If a name _is_ an email, the domain part gets ignored

```python
initials('joe@example.com') # 'jo'
```

When passing an Array of names, duplicates of initials are avoided

```python
initials(['John Doe', 'Jane Dane']) # ['JDo', 'JDa']
```

## Build and test

Install dependencies:

```shell
poetry install
```

Run the unit-tests:

```shell
poetry run pytest
```

## LICENSE

[ISC](LICENSE)
