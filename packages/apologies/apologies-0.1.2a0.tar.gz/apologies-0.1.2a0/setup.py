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
    'version': '0.1.2a0',
    'description': 'Python code to play a game similar to Sorry',
    'long_description': '# Apologies Python Library\n\n![](https://img.shields.io/pypi/l/apologies.svg)\n![](https://img.shields.io/pypi/wheel/apologies.svg)\n![](https://img.shields.io/pypi/pyversions/apologies.svg)\n![](https://github.com/pronovic/apologies/workflows/Test%20Suite/badge.svg)\n\n[Apologies](https://gitub.com/pronovic/apologies) is a Python library that\nimplements a game similar to the Sorry board game.  It includes a rudimentary\nway to play the game, intended for use by developers and not by end users.\n\nIt also serves as a complete example of how to manage a modern (circa 2020)\nPython project, including style checks, code formatting, integration with\nIntelliJ, CI builds at GitHub, and integration with PyPI and Read the Docs.\n\n*Note:* This is alpha-quality code that is still under active development.\nInterfaces may change without warning until the design stabilizes.\n\n',
    'author': 'Kenneth J. Pronovici',
    'author_email': 'pronovic@ieee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://apologies.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
