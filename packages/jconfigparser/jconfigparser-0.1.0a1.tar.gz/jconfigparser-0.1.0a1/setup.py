# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jconfigparser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jconfigparser',
    'version': '0.1.0a1',
    'description': 'Augmented python configparser',
    'long_description': None,
    'author': 'Florian Knoop',
    'author_email': 'florian_knoop@gmx.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
