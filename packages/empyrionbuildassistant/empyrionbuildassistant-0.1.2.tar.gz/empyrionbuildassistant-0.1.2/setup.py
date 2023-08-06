# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['empyrionbuildassistant', 'empyrionbuildassistant.lib']

package_data = \
{'': ['*']}

install_requires = \
['pathtools>=0.1.2,<0.2.0', 'vdf>=3.2,<4.0', 'watchdog>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['APPLICATION-NAME = entry:main']}

setup_kwargs = {
    'name': 'empyrionbuildassistant',
    'version': '0.1.2',
    'description': 'A simple set of scripts to make developing mods for Empyrion easier',
    'long_description': None,
    'author': 'Chris Wheeler',
    'author_email': 'cmwhee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
