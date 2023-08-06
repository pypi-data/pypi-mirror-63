# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tomlcheck']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cov>=2.8.1,<3.0.0', 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['tomlcheck = tomlcheck.run:run']}

setup_kwargs = {
    'name': 'tomlcheck',
    'version': '0.1.0',
    'description': 'A simple toml syntax checker',
    'long_description': None,
    'author': 'Arijit Basu',
    'author_email': 'sayanarijit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/sayanarijit/tomlcheck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
