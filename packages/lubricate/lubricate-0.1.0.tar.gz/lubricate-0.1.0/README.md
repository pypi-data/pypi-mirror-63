# lubricate

Lubricate helps you decrease friction when stuck at starting a project, no
matter if it's a scientific analysis or a Python package. It will initialise a
ready-to-use project structure with decent defaults.

# Installation

As easy as

    pip install lubricate

# Usage

Currently there are two types of projects available: `python` and `analysis`.
A `python` project is a fully configured Python package with tests, docs and
CI. An `analysis` is a scientific project.

## Create a Python package 

    lubricate new python foo
    
This will create the following folder structure (the virtualenv folder `venv` is collapsed for the sake of readability):

    ░ tamasgal@greybox.local:foopackage  master
    ░ 09:58:49 > tree -I venv
    .
    ├── CHANGELOG.rst
    ├── CONTRIBUTING.rst
    ├── LICENSE
    ├── MANIFEST.in
    ├── Makefile
    ├── README.rst
    ├── doc
    │   ├── Makefile
    │   ├── changelog.rst
    │   ├── conf.py
    │   ├── contribute.rst
    │   ├── index.rst
    │   └── user_guide.rst
    ├── foo
    │   ├── __init__.py
    │   ├── bar.py
    │   └── tests
    │       └── test_bar.py
    ├── pyproject.toml
    ├── requirements-dev.txt
    ├── requirements.txt
    ├── setup.py
    └── venv [collapsed folder]

    3 directories, 19 files
    
A virtualenv is created with the latest versions of `pip`, `setuptools` and `setuptools-scm` for version control:

    ░ tamasgal@greybox.local:foopackage  master
    ░ 10:01:06 > . venv/bin/activate
    ░ tamasgal@greybox.local:foopackage  master foopackage
    ░ 10:01:08 > pip list
    Package        Version
    -------------- -------
    pip            20.0.2
    setuptools     46.0.0
    setuptools-scm 3.5.0

## Get started with a new analysis project:

    lubricate new analysis the_analysis
