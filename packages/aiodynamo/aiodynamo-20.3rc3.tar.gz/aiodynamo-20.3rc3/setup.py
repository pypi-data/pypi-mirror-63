# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiodynamo', 'aiodynamo.http']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[aiohttp]>=3.6.2,<4.0.0',
 'httpx[httpx]>=0.11.1,<0.12.0',
 'yarl>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'aiodynamo',
    'version': '20.3rc3',
    'description': 'Asyncio DynamoDB client',
    'long_description': '# AsyncIO DynamoDB\n\n[![CircleCI](https://circleci.com/gh/HDE/aiodynamo.svg?style=svg&circle-token=ce893a3fdc37be4f5e9f0b44b8aa23e3c3c02f03)](https://circleci.com/gh/HDE/aiodynamo)\n\nAsynchronous, fast and pythonic DynamoDB client. See [the docs](https://aiodynamo.readthedocs.io/) for details.\n',
    'author': 'Jonas Obrist',
    'author_email': 'jonas.obrist@hennge.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HENNGE/aiodynamo',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
