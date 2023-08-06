![spacy syllables](https://raw.githubusercontent.com/sloev/spacy-syllables/master/header.jpg)

# Spacy Syllables

[![Build Status](https://travis-ci.org/sloev/spacy-syllables.svg?branch=master)](https://travis-ci.org/sloev/spacy-syllables) [![Latest Version](https://img.shields.io/pypi/v/spacy-syllables.svg)](https://pypi.python.org/pypi/spacy-syllables) [![Python Support](https://img.shields.io/pypi/pyversions/spacy-syllables.svg)](https://pypi.python.org/pypi/spacy-syllables)

A [spacy 2+ pipeline component](https://spacy.io/universe/category/pipeline) for adding multilingual syllable annotation to tokens. 

* Uses well established [pyphen](https://github.com/Kozea/Pyphen) for the syllables.
* Supports [a ton of languages](https://github.com/Kozea/Pyphen/tree/master/pyphen/dictionaries)
* Ease of use thx to the awesome pipeline framework in spacy

## Install

```bash
$ pip install spacy_syllables
```

which also installs the following dependencies:

* spacy = "^2.2.3"
* pyphen = "^0.9.5"

## Usage

The [`SpacySyllables`](spacy_syllables/__init__.py) class autodetects language from the given spacy nlp instance, but you can also override the detected language by specifying the `lang` parameter during instantiation, see how [here](tests/test_all.py).

### Normal usecase

```python

import spacy
from spacy_syllables import SpacySyllables

nlp = spacy.load("en_core_web_sm")

syllables = SpacySyllables(nlp)

nlp.add_pipe(syllables, after="tagger")

assert nlp.pipe_names == ["tagger", "syllables", "parser", "ner"]

doc = nlp("terribly long")

data = [(token.text, token._.syllables, token._.syllables_count) for token in doc]

assert data == [("terribly", ["ter", "ri", "bly"], 3), ("long", ["long"], 1)]

```

more examples in [tests](tests/test_all.py)


## Dev setup / testing

we are using
* [poetry](https://python-poetry.org/) for the package
* [nox](https://github.com/theacodes/nox) for the tests
* [pyenv](https://github.com/pyenv/pyenv) for specifying python versions for nox tests

### install

* [install pyenv](https://github.com/pyenv/pyenv#installation)
* [install poetry](https://python-poetry.org/docs/#installation)

then install the dev package and pyenv versions

```bash
$ poetry install
$ poetry --session install_pyenv_versions
```

### run tests

```bash
$ poetry run nox
```
