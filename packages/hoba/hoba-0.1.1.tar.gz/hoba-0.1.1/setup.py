# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hoba']

package_data = \
{'': ['*']}

install_requires = \
['fire',
 'gitpython',
 'keyring',
 'keyrings.alt',
 'loguru',
 'pyaml',
 'python-gnupg',
 'shellingham']

entry_points = \
{'console_scripts': ['hoba = hoba.cli:main']}

setup_kwargs = {
    'name': 'hoba',
    'version': '0.1.1',
    'description': 'Yet another secrets management toolkit',
    'long_description': None,
    'author': 'Michael Zaikin',
    'author_email': 'mz@baking-bad.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
