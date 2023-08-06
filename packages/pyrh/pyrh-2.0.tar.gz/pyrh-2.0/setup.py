# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrh']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8,<3.0', 'requests>=2.23,<3.0', 'six>=1.14,<2.0']

extras_require = \
{':python_version >= "2.7" and python_version < "2.8"': ['configparser>=3.5,<4.0',
                                                         'enum>=0.4.6,<0.5.0']}

setup_kwargs = {
    'name': 'pyrh',
    'version': '2.0',
    'description': 'Unofficial Robinhood Python API',
    'long_description': "[![robinhood-logo](./docs/logo-color-transparent.png)](https://github.com/robinhood-unofficial/Robinhood)\n------------\n\n# pyrh - Unofficial Robinhood API\n\n\n[![Gitter](https://img.shields.io/gitter/room/J-Robinhood/Lobby)](https://gitter.im/J-Robinhood/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![GitHub](https://img.shields.io/github/license/robinhood-unofficial/Robinhood)](https://github.com/robinhood-unofficial/Robinhood/blob/master/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPython Framework to make trades with Robinhood Private API.\nSee the original [blog post](https://medium.com/@rohanpai25/reversing-robinhood-free-accessible-automated-stock-trading-f40fba1e7d8b).\n\nSupports Python 2.7+ and 3.6+\n\n## Current Features\n- Placing buy orders (`Robinhood.place_buy_order`)\n- Placing sell order (`Robinhood.place_sell_order`)\n- Fetch and cancel orders (`Robinhood.order_history` and `Robinhood.cancel_order`)\n- Quote information (`Robinhood.quote_data`)\n- User portfolio data (`Robinhood.portfolios`)\n- User positions data (`Robinhood.positions`)\n- More coming soon\n\n### How To Install:\nClone the repository into your project directory using:\n\n```\ngit clone https://github.com/robinhood-unofficial/Robinhood\n```\n\nThen navigate to the cloned directory, where `setup.py` is located. Now run the following to install:\n\n```\npip install .\n```\n\n### Converting to Python 3\nProject will work on both python 2 and python 3\n\n### Running [example.py](https://github.com/robinhood-unofficial/Robinhood/blob/master/docs/example.ipynb)\n* Install jupyter\n```\npip install jupyter\njupyter notebook\n```\n\nThen navigate to the example file linked above and run it.\n\n### Data returned\n* Quote data\n  + Ask Price\n  + Ask Size\n  + Bid Price\n  + Bid Size\n  + Last trade price\n  + Previous close\n  + Previous close date\n  + Adjusted previous close\n  + Trading halted\n  + Updated at\n  + Historical Price\n* User portfolio data\n  + Adjusted equity previous close\n  + Equity\n  + Equity previous close\n  + Excess margin\n  + Extended hours equity\n  + Extended hours market value\n  + Last core equity\n  + Last core market value\n  + Market value\n  + Order history\n  + Dividend history\n* User positions data\n  + Securities owned\n* News\n\n------------------\n\n# Changelog\n## 2.0\n* Fixed 2fa connection issues\n* Last version to support python 2\n\n## 1.0.1\n* Added custom exception\n\n# Developer setup\n* Python 3.7+ is required\n* poetry is used to manage package dependencies\n* pre-commit is used to manage the project's tooling and linting\n  * black\n  * flake8\n```\nbrew install poetry\nbrew install pre-commit\npoetry install\npre-commit install\n```\n\nTo manually run the linting checks. They are automatically run when you try to push the\ncode.\n```\npre-commit run -a\n```\n\n# Related\n* [robinhood-ruby](https://github.com/rememberlenny/robinhood-ruby) - RubyGem for interacting with Robinhood API\n* [robinhood-node](https://github.com/aurbano/robinhood-node) - NodeJS module to make trades with Robinhood Private API\n",
    'author': 'Unofficial Robinhood Python API Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/georgianpartners/foreshadow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
