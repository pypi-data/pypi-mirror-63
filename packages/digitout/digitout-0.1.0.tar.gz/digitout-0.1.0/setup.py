# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['digitout']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0',
 'npyscreen>=4.10.5,<5.0.0',
 'od>=1.0,<2.0',
 'toml>=0.10.0,<0.11.0',
 'xdg>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'digitout',
    'version': '0.1.0',
    'description': 'Seek data structures of your Python application.',
    'long_description': None,
    'author': 'Grzegorz Krason',
    'author_email': 'grzegorz.krason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
