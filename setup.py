from distutils.core import setup

setup(
    name='tryingsnake',
    version='0.2.1',
    packages=['tryingsnake'],
    url='https://github.com/zero323/tryingsnake',
    license='MIT',
    author='Maciej Szymkiewicz',
    author_email='matthew.szymkiewicz@gmail.com',
    description='Exception handling, the functional way.',
    package_data={'tryingsnake': ['test/*.py']},
    long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
    classifiers=['Development Status :: 3 - Alpha'],
    zip_safe=False
)
