# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apologies']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'apologies',
    'version': '0.1.0a0',
    'description': 'Python code to play a game similar to Sorry',
    'long_description': "# Apologies Python Library\n\n![](https://github.com/pronovic/apologies/workflows/Test%20Suite/badge.svg)\n\nThis is a Python library that implements a game similar to the Sorry\nboard game.  It includes a rudimentary way to play the game, intended\nfor use by developers and not by end users.\n\nIt also serves as a complete example of how to manage a modern (circa 2020)\nPython project, including style checks, code formatting, integration with\nIntelliJ, continuous integration at GitHub, etc.\n\n## Developer Notes\n\n### Development Environment\n\nMy primary development environment is IntelliJ (or just Vim) on MacOS.  Notes\nbelow assume that environment, although most of this should work the same on\nWindows or Linux.\n\n### Packaging and Dependencies\n\nThis project uses [Poetry](https://python-poetry.org/) to manage Python\npackaging and dependencies.  Most day-to-day tasks (such as running unit \ntests from the command line) are orchestrated through Poetry.  A coding\nstandard is enforced using [Black](https://github.com/psf/black) and [PyLint](https://www.pylint.org/).\n\n### Developer Prequisites\n\nBefore starting, install the following tools using [Homebrew](https://brew.sh/)\nor the package manager for your platform:\n\n```shell\nbrew install python3\nbrew install poetry\nbrew install black\nbrew install pylint\n```\n\nYou need to install all of these tools before you can do local development or\ncommit code using the standard process, due to the pre-commit hooks (see\nbelow).\n\nOptionally, you may also install the following:\n\n```shell\nbrew install pre-commit   # to adjust pre-commit hooks\nbrew install make         # if you want to build Sphinx documentation\n```\n\n### Pre-Commit Hooks\n\nThere are local pre-commit hooks that depend on Black and Pylint, so the code\nis properly-formatted and lint-clean when it's checked in.  If you don't\ninstall Black and Pylint as described above, then you won't be able to commit\nyour changes.\n\nIf necessary, you can temporarily [disable a hook](https://pre-commit.com/#temporarily-disabling-hooks)\nor even remove the hook with `pre-commit uninstall`.\n\n### Activating the Virtual Environment\n\nPoetry manages the virtual environment used for testing.  Theoretically, the\nPoetry `shell` command gives you a shell using that virutalenv.  However, it\ndoesn't work that well.  Instead, it's simpler to just activate the virtual\nenvironment directly.  The [`run`](run) script has an entry that dumps out the\ncorrect `source` command. Otherwise, see [`notes/venv.sh`](notes/venv.sh) for a way\nto set up a global alias that activates any virtualenv found in the current\ndirectory.\n\n### Developer Tasks\n\nThe [`run`](run) script provides shortcuts for common developer tasks:\n\n```\n$ run --help\n\n------------------------------------\nShortcuts for common developer tasks\n------------------------------------\n\nUsage: run <command>\n\n- run install: Setup the virtualenv via Poetry\n- run activate: Print command needed to activate the Poetry virtualenv\n- run lint: Run the Pylint code checker\n- run format: Run the Black code formatter\n- run test: Run the unit tests\n- run test -c: Run the unit tests with coverage\n- run test -ch: Run the unit tests with coverage and open the HTML report\n- run tox: Run the broader Tox test suite used by the GitHub CI action\n- run docs: Build the Spinx documentation for apologies.readthedocs.io\n- run publish: Tag the current code and publish to PyPI\n```\n",
    'author': 'Kenneth J. Pronovici',
    'author_email': 'pronovic@ieee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pronovic/apologies',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
