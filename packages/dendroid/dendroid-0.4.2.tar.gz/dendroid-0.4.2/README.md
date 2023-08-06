dendroid
========

[![](https://travis-ci.com/lycantropos/dendroid.svg?branch=master)](https://travis-ci.com/lycantropos/dendroid "Travis CI")
[![](https://dev.azure.com/lycantropos/dendroid/_apis/build/status/lycantropos.dendroid?branchName=master)](https://dev.azure.com/lycantropos/dendroid/_build/latest?definitionId=14&branchName=master "Azure Pipelines")
[![](https://codecov.io/gh/lycantropos/dendroid/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/dendroid "Codecov")
[![](https://img.shields.io/github/license/lycantropos/dendroid.svg)](https://github.com/lycantropos/dendroid/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/dendroid.svg)](https://badge.fury.io/py/dendroid "PyPI")

In what follows
- `python` is an alias for `python3.5` or any later
version (`python3.6` and so on),
- `pypy` is an alias for `pypy3.5` or any later
version (`pypy3.6` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions:
- with `CPython`
  ```bash
  python -m pip install --upgrade pip setuptools
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade pip setuptools
  ```

### User

Download and install the latest stable version from `PyPI` repository:
- with `CPython`
  ```bash
  python -m pip install --upgrade dendroid
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade dendroid
  ```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/dendroid.git
cd dendroid
```

Install dependencies:
- with `CPython`
  ```bash
  python -m pip install --force-reinstall -r requirements.txt
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --force-reinstall -r requirements.txt
  ```

Install:
- with `CPython`
  ```bash
  python setup.py install
  ```
- with `PyPy`
  ```bash
  pypy setup.py install
  ```

Usage
-----

```python
>>> from dendroid import avl, red_black, splay
>>> avl_tree, red_black_tree, splay_tree = (avl.tree(), 
...                                         red_black.tree(), 
...                                         splay.tree())
>>> 1 not in avl_tree and 1 not in red_black_tree and 1 not in splay_tree
True
>>> len(avl_tree) == len(red_black_tree) == len(splay_tree) == 0
True
>>> list(avl_tree) == list(red_black_tree) == list(splay_tree) == []
True
>>> avl_tree.add(1)
>>> red_black_tree.add(1)
>>> splay_tree.add(1)
>>> 1 in avl_tree and 1 in red_black_tree and 1 in splay_tree
True
>>> len(avl_tree) == len(red_black_tree) == len(splay_tree) == 1
True
>>> list(avl_tree) == list(red_black_tree) == list(splay_tree) == [1]
True
>>> avl_tree.remove(1)
>>> red_black_tree.remove(1)
>>> splay_tree.remove(1)
>>> 1 not in avl_tree and 1 not in red_black_tree and 1 not in splay_tree
True
>>> len(avl_tree) == len(red_black_tree) == len(splay_tree) == 0
True
>>> list(avl_tree) == list(red_black_tree) == list(splay_tree) == []
True

```

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose release
```

Bump version
```bash
bump2version --verbose release
```

This will set version to `major.minor.patch`.

### Running tests

Install dependencies:
- with `CPython`
  ```bash
  python -m pip install --force-reinstall -r requirements-tests.txt
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --force-reinstall -r requirements-tests.txt
  ```

Plain
```bash
pytest
```

Inside `Docker` container:
- with `CPython`
  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```
- with `PyPy`
  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

`Bash` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```bash
  ./run-tests.sh
  ```
  or
  ```bash
  ./run-tests.sh cpython
  ```

- with `PyPy`
  ```bash
  ./run-tests.sh pypy
  ```

`PowerShell` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```powershell
  .\run-tests.ps1
  ```
  or
  ```powershell
  .\run-tests.ps1 cpython
  ```
- with `PyPy`
  ```powershell
  .\run-tests.ps1 pypy
  ```
