# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mygp_cli']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['mygp-cli = mygp_cli.main:main']}

setup_kwargs = {
    'name': 'mygp-cli',
    'version': '0.0.4.dev1',
    'description': 'Command-line interface for the Marketplace Sandbox API',
    'long_description': None,
    'author': 'Igor Brejc',
    'author_email': 'igor.brejc@nfcsb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
