#!/usr/bin/env python
# pylama:ignore=E221,E251

from setuptools import find_packages, setup

setup(
    name         = 'innerjoin',
    version      = '1.0',
    description  = 'Cerebras Inner Join Exercise',
    author       = 'Gustavo Gama',
    author_email = 'gustavo.gama@gmail.com',
    url          = 'https://gama.igenesis.com.br',
    packages     = find_packages()
)
