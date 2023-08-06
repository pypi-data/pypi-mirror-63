# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fafi']
install_requires = \
['appdirs>=1.4.3,<2.0.0', 'click>=7.1.1,<8.0.0', 'newspaper3k>=0.2.8,<0.3.0']

entry_points = \
{'console_scripts': ['fafi = poetry.console:cli']}

setup_kwargs = {
    'name': 'fafi',
    'version': '0.1.3',
    'description': 'CLI for indexing Firefox bookmarks.',
    'long_description': None,
    'author': 'Sander van Dragt',
    'author_email': 'sander@vandragt.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
