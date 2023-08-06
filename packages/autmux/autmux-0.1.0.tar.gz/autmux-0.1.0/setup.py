# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autmux',
 'autmux.console',
 'autmux.scenarios',
 'autmux.scenarios.jobs',
 'autmux.tmux']

package_data = \
{'': ['*']}

install_requires = \
['PyYaml>=5.3,<6.0', 'click-help-colors>=0.7,<0.8', 'click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['autmux = autmux.console:main']}

setup_kwargs = {
    'name': 'autmux',
    'version': '0.1.0',
    'description': 'Automatically manipulating tmux',
    'long_description': None,
    'author': 'Hiroki Konishi',
    'author_email': 'relastle@gmail.com',
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
