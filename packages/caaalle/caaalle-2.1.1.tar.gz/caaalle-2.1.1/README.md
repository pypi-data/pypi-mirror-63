# caaalle

[![image](https://img.shields.io/pypi/v/caaalle.svg)](https://pypi.org/project/caaalle/)
[![Build Status](https://github.com/caalle/caaalle/workflows/Release/badge.svg)](https://github.com/caalle/caaalle/workflows/Release/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/caaalle/badge/?version=latest)](https://caaalle.readthedocs.io/en/latest/?badge=latest)

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```bash
pip3 install caaalle
```

### Project Dependencies

We use [pipenv](https://docs.pipenv.org) for managing project dependencies and Python environments (i.e. virtual environments). These dependencies are **not** to be confused with the package installation dependencies for the package under developement - i.e. those that need to be defined in the `install_requires` section of `setup.py`. All of the direct packages dependencies required to run the project's code (e.g. NumPy for tensors), as well as all the packages used during development (e.g. flake8 for code linting and IPython for interactive console sessions), are described in the `Pipfile`. Their precise downstream dependencies are crystallised in `Pipfile.lock`, which is used to guarentee repeatable (i.e. deterministic) builds.

#### Installing Pipenv

To get started with Pipenv, first of all download it - assuming that there is a 'global' version of Python available on your system and on the PATH, then this can be achieved by running the following command,

```bash
pip3 install pipenv
```

For more information, including advanced configuration options, see the [official pipenv documentation](https://docs.pipenv.org).

#### Installing this Projects' Dependencies

Make sure that you're in the project's root directory (the same one in which `Pipfile` resides), and then run,

```bash
pipenv install --dev
```

This will install all of the direct project dependencies as well as the development dependencies (the latter a consequence of the `--dev` flag). To add and remove dependencies as required for your new project, use `pipenv install` and `pipenv uninstall` as required, using the `--dev` flag for development-only dependencies.

#### Running Python and IPython from the Project's Virtual Environment

In order to open a Python REPL using within an environment that precisely mimics the one the project is being developed with, use Pipenv from the command line as follows,

```bash
pipenv run python3
```

The `python3` command could just as well be `ipython3`.

### Running Unit Tests

All test have been written using the [PyTest](https://docs.pytest.org/en/latest/) package. Tests are kept in the `tests` folder and can be run from the command line by - e.g. by invoking,

```bash
pipenv run pytest
```

The test suite is structured as an independent Python package as follows:

```bash
tests/
 |   __init__.py
 |   conftest.py
 |   test_caaalle.py
```

The `conftest.py` module is used by PyTest - in this particular instance for loading test data and building objects that will then be used by potentially many other tests. These are referred to as 'fixtures' in PyTest - more details can be found [here](https://docs.pytest.org/en/latest/fixture.html).

### Linting Code

I prefer to use [flake8](http://flake8.pycqa.org/en/latest/) for style guide enforcement. This can be invoked from the command line by running,

```bash
pipenv run flake8 caaalle
```

### Static Type Checking

We have used the Python type annotation framework, together with the [MyPy package](http://mypy-lang.org), to perform static type checks on the codebase. Analogous to any linter or unit testing framework, MyPy can be run from the command line as follows,

```bash
pipenv run python -m mypy caaalle/*.py
```

MyPy options for this project can be defined in the `mypy.ini` file that MyPy will look for by default. For more information on the full set of options, see the [mypy documentation](https://mypy.readthedocs.io/en/stable/config_file.html).

Examples of type annotation and type checking for library development can be found in the `py_pkg.curves.py` module. This should also be cross-referenced with the improvement to readability (and usability) that this has on package documentation.

### Documentation

The documentation in the `docs` folder has been built using [Sphinx](http://www.sphinx-doc.org). We have used the default 'quickstart' automatic configuration, which was originally triggered by executing,

```bash
pipenv run sphinx-quickstart
```

The output is based primarily on the Docstrings in the source code, using the `autodoc` extension within Sphinx (specified during the 'quickstart'). The contents for the entry point into the docs (`index.html`), is defined in the `index.rst` file, which itself imports the `modules.rst` file that lists all of the modules to document. The documentation can be built by running the following command,

```bash
pipenv run sphinx-build -b html docs/source docs/build_html
```

The resulting HTML documentation can be accessed by opening `docs/build_html/index.html` in a web browser.

My preferred third party theme from [Read the Docs](https://readthedocs.org) has also been used, by installing the `sphinx_rtd_theme` as a development dependency and modifying `docs/source/config.py` as follows:

```python
import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
```

### Building Deployable Distributions

The recommended (and most pragmatic) way of deploy this package is to build a Python [wheel](https://wheel.readthedocs.io/en/stable/) and to then to install it in a fresh virtual environment on the target system. The exact build configuration is determined by the parameters in `setup.py`. Note, that this requires that all package dependencies also be specified in the `install_requires` declaration in `setup.py`, **regardless** of their entry in `Pipfile`. For more information on Python packaging refer to the [Python Packaging User Guide](https://packaging.python.org) and the accompanying [sample project](https://github.com/pypa/sampleproject). To create the Python wheel run,

```bash
pipenv run python setup.py bdist_wheel
```

This will create `build`, `caaalle.egg-info` and `dist` directories - the wheel can be found in the latter. This needs to be copied to the target system (which we are assuming has Python and Pipenv available as a minimum), where it can be installed into a new virtual environment, together with all downstream dependencies, using,

```bash
pipenv install path/to/your-package.whl
```

### Automated Testing and Deployment using Travis CI

We have chosen Travis for Continuous Integration (CI) as it integrates very easily with Python and GitHub (where I have granted it access to my public repositories). The configuration details are kept in the `.travis.yaml` file in the root directory:

```yaml
ncsudo: required

language: python

python:
  - 3.7-dev

install:
  - pip install pipenv
  - pipenv install --dev

script:
  - pipenv run pytest

deploy:
  provider: pypi
  user: __token__
  password:
    secure: my-encrypted-pypi-password
  on:
    tags: true
  distributions: bdist_wheel
```
