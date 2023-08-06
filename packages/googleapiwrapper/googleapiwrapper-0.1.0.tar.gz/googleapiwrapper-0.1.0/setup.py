# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['googleapiwrapper']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'googleapiwrapper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ethan mak',
    'author_email': 'ethan.mak@streetsine.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
