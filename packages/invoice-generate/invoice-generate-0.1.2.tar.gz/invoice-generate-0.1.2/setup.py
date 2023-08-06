# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invoice_generate']

package_data = \
{'': ['*'], 'invoice_generate': ['templates/*']}

install_requires = \
['click>=7.0,<8.0',
 'jinja2>=2.10.3,<3.0.0',
 'pdfkit>=0.6.1,<0.7.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['invoice-generate = invoice_generate:main']}

setup_kwargs = {
    'name': 'invoice-generate',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Eric Prykhodko',
    'author_email': 'eprykhodko@bcdtriptech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
