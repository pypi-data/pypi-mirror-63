#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    find_packages,
    setup,
)

extras_require = {
    'linter': [
        "flake8==3.7.8",
        "isort>=4.2.15,<4.3.22",
    ],
    'dev': [
        "bumpversion==0.5.3",
        "pytest==5.2.1",
        "click==7.0",
        "twine==1.12.1",
        "mock==3.0.5",
        "when-changed",
        "Random-Word==1.0.4",
        "pytest-cov==2.8.1"
    ],
    'hw-wallet': [
        "ledgerblue==0.1.29"
    ]
}

extras_require['dev'] = (
    extras_require['linter'] + extras_require['dev'] + extras_require['hw-wallet']
)

setup(
    name='skale.py',
    version='',
    description='SKALE client tools',
    long_description_markdown_filename='README.md',
    author='SKALE Labs',
    author_email='support@skalelabs.com',
    url='https://github.com/skalenetwork/skale.py',
    include_package_data=True,
    install_requires=[
        "web3==5.2.2",
        "asyncio==3.4.3",
        "pyyaml==5.1.2",
        "sgx.py==0.3dev0",
    ],

    python_requires='>=3.6,<4',
    extras_require=extras_require,



    keywords='skale',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],

    package_data={  # Optional
        'contracts': ['utils/contracts_data.json', 'envs/envs.yml', 'envs/aws.json'],
    },
)
