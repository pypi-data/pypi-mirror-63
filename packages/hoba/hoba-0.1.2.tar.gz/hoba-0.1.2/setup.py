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
    'version': '0.1.2',
    'description': 'Yet another secrets management toolkit',
    'long_description': '# Hoba\n\n\n[![PyPI version](https://badge.fury.io/py/hoba.svg?)](https://badge.fury.io/py/hoba)\n[![Build Status](https://travis-ci.org/m-kus/hoba.svg?branch=master)](https://travis-ci.org/m-kus/hoba)\n[![Made With](https://img.shields.io/badge/made%20with-python-blue.svg?)](https://www.python.org)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nYet another secrets management toolkit based on [passwordstore](https://www.passwordstore.org/)\n\n![hoba](http://memesmix.net/media/download.php?meme=weqlu4)\n\n\n## Requirements\n\n* git\n* gnupg\n* pass\n* python 3.6+\n* pip 19.0.1+\n\n## Installation\n\n```\n$ pip install git+https://github.com/m-kus/hoba\n```\n\n## Usage\n\nAll hoba commands work only if there is a ```hoba.yml``` file inside the current directory. File format will be described below.\n\n### Storing and sharing secrets\n\nPass is a great alternative to Hashicorp Vault and other enterprise secret storages, cause it\'s simple, safe, and portable. In my team we came to a pretty convenient scheme without loosing in security.\n\n1. All passwords encryption key, api keys, certificates, etc. are kept in a pass repo, which is gpg-encrypted and stored in git;\n2. Pass allows to implement simple access control policy for each tree node with inheritance;\n3. Each developer has to generate gpg key and add pubkey to the pass repo (keys are stored in .gpg-keys file);\n4. All developers have to import all keys from the repo and set maximum trust level;\n\nYou can do this manually, but there is a command which does pretty much the same:\n\n```\n$ hoba sync\n```\n\nHoba can also spawn a shell with overrided `PASSWORD_STORE_DIR` environment variable:\n\n```\n$ hoba shell\n$ pass\n```\n\n### Deploying secrets\n\nBy default hoba looks for a ```default``` section inside the configuration file.\n\n```\n$ hoba gen\n```\n\nYou can also specify target env:\n\n```\n$ hoba gen dev\n```\n\nSample hoba configuration file:\n\n```yaml\npassword-store:\n  repo_url: http://github.com/example.git\n  repo_dir: ./.password-store\n  \nenvironments:\n  dev:\n    default:\n  prod:\n  \ntargets:\n  - type: env_file\n    output: ./.secrets/{ENV}.env\n    variables:\n      - DB_PASSWORD={ENV}/postgresql/password\n    except:\n      - dev\n\n  - type: dir\n    output: ./.secrets\n    files:\n      - ssl/example.com/cert_key:ssl/cert_key\n      - ssl/example.com/dh_params:ssl/dh_params\n    only:\n      - prod\n\n  - type: keyring\n    output: ./.secrets/keyring_pass.cfg\n    entries:\n      - app@telegram:{ENV}/telegram/bot_api_key\n```\n\nDocker compose integration example:\n\n```yaml\nversion: "3.1"\nservices:\n  nginx:\n    environment:\n      env_file:\n      - ./.secrets/dev.env\n    secrets:\n      - cert_key\n      - dh_params\n      - source: keyring\n        target: /root/.local/share/python_keyring/keyring_pass.cfg\n    \nsecrets:\n  cert_key:\n    file: ./.secrets/ssl/cert_key\n  dh_params:\n    file: ./.secrets/ssl/dh_params\n  keyring:\n    file: ./.secrets/keyring_pass.cfg\n```\n',
    'author': 'Michael Zaikin',
    'author_email': 'mz@baking-bad.org',
    'url': 'https://github.com/m-kus/hoba',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
