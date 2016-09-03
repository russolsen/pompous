# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pompous',
    version='0.0.1',
    description='Simple assembler for Python',
    long_description=readme,
    scripts=['bin/pompous'],
    author='Russ Olsen',
    author_email='russ@russolsen.com',
    url='https://github.com/russolsen/pompous',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

