#!/bin/env python3

from setuptools import setup

setup(
    name='SnowSQL',
    version='0.1.3',
    description='Python light database framework for sqlite3 mysql/mariadb',
    author='Tyan Boot',
    author_email='tyanboot@outlook.com',
    url='https://github.com/tyan-boot/SnowSQL',
    packages=['SnowSQL', 'SnowSQL.Handlers'],
    keywords='database sql framework'
)
