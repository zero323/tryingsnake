#!/usr/bin/env python

from os.path import exists
from distutils.core import setup
import tryingsnake

setup(
    name='tryingsnake',
    version=tryingsnake.__version__,
    packages=['tryingsnake'],
    url='https://github.com/zero323/tryingsnake',
    license='MIT',
    author='Maciej Szymkiewicz',
    author_email='matthew.szymkiewicz@gmail.com',
    description='Exception handling, the functional way.',
    package_data={'tryingsnake': ['test/*.py']},
    long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License'],
    zip_safe=False
)
