# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splitsio']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses_json>=0.4.2,<0.5.0', 'marshmallow>=3.5.1,<4.0.0']

setup_kwargs = {
    'name': 'splitsio',
    'version': '0.1.0',
    'description': 'A Python implementation of the splits.io REST API.',
    'long_description': None,
    'author': 'Jeremy Silver',
    'author_email': 'jeremyag@comcast.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
