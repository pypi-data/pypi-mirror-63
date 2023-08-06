# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rli', 'rli.commands', 'rli.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.47,<2.0', 'click>=7.1.1,<8.0.0']

entry_points = \
{'console_scripts': ['rli = rli.cli:cli']}

setup_kwargs = {
    'name': 'rli',
    'version': '0.0.2',
    'description': 'My CLI tool to automate common tasks.',
    'long_description': None,
    'author': 'luke.shay',
    'author_email': 'luke.shay@vertexvis.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
