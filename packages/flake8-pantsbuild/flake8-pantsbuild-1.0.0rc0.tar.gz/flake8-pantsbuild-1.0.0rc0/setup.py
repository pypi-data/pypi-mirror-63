# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_pantsbuild']
install_requires = \
['flake8>=3.7']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.3.0']}

entry_points = \
{u'flake8.extension': ['PB1 = flake8_pantsbuild:Plugin',
                       'PB2 = flake8_pantsbuild:IndentationPlugin',
                       'PB3 = flake8_pantsbuild:TrailingSlashesPlugin',
                       'PB6 = flake8_pantsbuild:SixPlugin']}

setup_kwargs = {
    'name': 'flake8-pantsbuild',
    'version': '1.0.0rc0',
    'description': 'Various Flake8 lints used by the Pants project and its users.',
    'long_description': None,
    'author': 'Pantsbuild developers',
    'author_email': 'pantsbuild@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
