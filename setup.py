#!/usr/bin/env python

from os.path import exists
from setuptools import setup
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
    long_description=(open('README.md').read() if exists('README.md')
                        else ''),
    long_description_content_type="text/markdown",
    classifiers=['Programming Language :: Python :: 3',
                 'Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License'],
    tests_require=['pytest'],
    zip_safe=False,
)
