# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coronaviruspy']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=7.1.1,<8.0.0',
 'requests>=2.23.0,<3.0.0',
 'termgraph>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['cinfo = coronaviruspy.cli:coronavirus']}

setup_kwargs = {
    'name': 'coronaviruspy',
    'version': '0.1.0',
    'description': 'CLI command for showing coronavirus info',
    'long_description': None,
    'author': 'Daniel Kukucz',
    'author_email': 'daniel@kukucz.com',
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
