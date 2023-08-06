# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unholster_inbox']

package_data = \
{'': ['*']}

install_requires = \
['aws>=0.2.5,<0.3.0', 'boto3>=1.12.23,<2.0.0', 'click>=7.1.1,<8.0.0']

setup_kwargs = {
    'name': 'unholster-inbox',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Sebastián Acuña',
    'author_email': 'sebastian@unholster.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
