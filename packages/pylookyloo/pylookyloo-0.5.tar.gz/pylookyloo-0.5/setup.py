# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylookyloo']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['lookyloo = pylookyloo:main']}

setup_kwargs = {
    'name': 'pylookyloo',
    'version': '0.5',
    'description': 'Python client for Lookyloo',
    'long_description': None,
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CIRCL/lookyloo/client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
