# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiopvpc']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6,<4.0', 'async_timeout>=3.0,<4.0', 'pytz>=2019.3,<2020.0']

setup_kwargs = {
    'name': 'aiopvpc',
    'version': '1.0.0',
    'description': 'PVPC Spanish Electricity prices retrieval',
    'long_description': '[![PyPi](https://pypip.in/v/aiopvpc/badge.svg)](https://pypi.org/project/aiopvpc/)\n[![Wheel](https://pypip.in/wheel/aiopvpc/badge.svg)](https://pypi.org/project/aiopvpc/)\n[![Travis Status](https://travis-ci.org/azogue/aiopvpc.svg?branch=master)](https://travis-ci.org/azogue/aiopvpc)\n\n# aiopvpc\n\nSimple aio library to download Spanish electricity hourly prices.\n\nMade to support the [**`pvpc_hourly_pricing`** HomeAssistant integration](https://www.home-assistant.io/integrations/pvpc_hourly_pricing/).\n\n<span class="badge-buymeacoffee"><a href="https://www.buymeacoffee.com/azogue" title="Donate to this project using Buy Me A Coffee"><img src="https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg" alt="Buy Me A Coffee donate button" /></a></span>\n',
    'author': 'Eugenio Panadero',
    'author_email': 'eugenio.panadero@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/azogue/aiopvpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
