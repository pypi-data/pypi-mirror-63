# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['countdown']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'countdown',
    'version': '0.1.0',
    'description': 'Package to solve the number round from the Channel 4 television show "Countdown"',
    'long_description': None,
    'author': 'Valentin Calomme',
    'author_email': 'info@valentincalomme.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
