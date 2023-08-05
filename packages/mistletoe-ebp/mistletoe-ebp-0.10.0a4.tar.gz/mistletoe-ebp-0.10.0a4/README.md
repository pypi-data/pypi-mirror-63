# mistletoe-ebp

[![CI Status][travis-badge]][travis-link]
[![Coverage][coveralls-badge]][coveralls-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![Code style: black][black-badge]][black-link]
[![PyPI][pypi-badge]][pypi-link]
[![Conda][conda-badge]][conda-link]

This is a version of [mistletoe] maintained by the [Excutable Book Project (EBP)][ebp-link]. It tracks the `myst` branch of [ExecutableBookProject/mistletoe](https://github.com/ExecutableBookProject/mistletoe)
which eventually, it is hoped, will be merged into mistletoe itself.

mistletoe is a Markdown parser in pure Python,
designed to be fast, spec-compliant and fully customizable.

Apart from being the fastest
CommonMark-compliant Markdown parser implementation in pure Python,
mistletoe also supports easy definitions of custom tokens.
Parsing Markdown into an abstract syntax tree
also allows us to swap out renderers for different output formats,
without touching any of the core components.

Unfortunately, mistletoe is not currently being actively maintained
(as of June 8th 2019), and so this fork has been created to allow for a
deployed release that can be utilised by EBP. Here is a working list of 'up-streamable' changes that would be desired of mistletoe that this version has begun to implement:

- [x] Move testing from `unittest` to `pytest`: `pytest` is now the *de facto* testing architecture and vastly improves the usability/flexibility of testing.
- [x] Introduce `pre-commit` code linting and formatting: This standardizes the code style across the package, and ensures that new commits and Pull Requests also conform to it.
- [x] Introduce `ReadTheDocs` documentation
- [x] Add a conda-forge distribution of the package
- [x] Improve the AST API and documentation: I view [panflute](http://scorreia.com/software/panflute/index.html)'s implementation of the pandoc API in python, as the gold standard for how a pythonic AST API should be written and documented. Some tweaks to the current token class objects, and creating auto-generated RTD documentation, could achieve this.
- [ ] Storage of source line/column ranges: LSP and good rendering reporting of warnings/errors, requires access to the source line and column ranges of each parsed token.
- [x] Asynchronous parsing: LSP requires documents to be parsed asynchronously. Currently, mistletoe contains a number of global state objects, which make parsing inherently not thread-safe. The simple solution to this is to store these items as `threading.local` objects. A related but slightly more complete solution is to introduce the idea of a 'scoped session', similar to that used by sqlalchemy for database access: [Contextual/Thread-local Sessions](https://docs.sqlalchemy.org/en/13/orm/contextual.html#unitofwork-contextual)
- [x] Improve extensibility of block tokens: A Markdown parser is inherently a Finite State-Machine + Memory (a.k.a Push-down Automata (PDA)), with parsing tokens as states (for a good example of a python state-machine see [pytransitions](https://github.com/pytransitions/transitions)). The problem with extensibility, is that inherently states are interdependent; when introducing a new state/token you must provide logic to all the other tokens, w.r.t to when to transition to this new token. Currently, MyST Parser sub-classes nearly all the Mistletoe block tokens to implement the extensions it requires, but it would be ideal if there was a more systematic approach for this.
- [ ] Improve extensibility for span tokens: Mistletoe does allow for span token extensions to be added, at least in a simple way. However, as with block tokens above, there is often an interconnectivity to them, especially when considering nested span tokens. As of 7cc2c92, MyST-Parser now overrides some of Mistetoe's core logic to achieve correct parsing of Math tokens, but if possible this should be made more general.
- [ ] Improve rendering logic: Currently, there is no concept of recursive walk-throughs or 'visitor' patterns in the Misteltoe `BaseRenderer`, which is a better method for rendering tree like structures (as used by docutils/panflute). Also, the current token instantiating (within context managers) needs improvement (see [miyuchina/mistletoe#56](https://github.com/miyuchina/mistletoe/issues/56)).

[mistletoe]: https://github.com/miyuchina/mistletoe
[ebp-link]: https://github.com/ExecutableBookProject
[travis-badge]: https://travis-ci.org/ExecutableBookProject/mistletoe-ebp.svg?branch=master
[travis-link]: https://travis-ci.org/ExecutableBookProject/mistletoe-ebp
[coveralls-badge]: https://coveralls.io/repos/github/ExecutableBookProject/mistletoe-ebp/badge.svg?branch=master
[coveralls-link]: https://coveralls.io/github/ExecutableBookProject/mistletoe-ebp?branch=master
[rtd-badge]: https://readthedocs.org/projects/mistletoe-ebp/badge/?version=latest
[rtd-link]: https://mistletoe-ebp.readthedocs.io/en/latest/?badge=latest
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[pypi-badge]: https://img.shields.io/pypi/v/mistletoe-ebp.svg
[pypi-link]: https://pypi.org/project/mistletoe-ebp
[conda-badge]: https://anaconda.org/conda-forge/mistletoe-ebp/badges/version.svg
[conda-link]: https://anaconda.org/conda-forge/mistletoe-ebp
[black-link]: https://github.com/ambv/black
