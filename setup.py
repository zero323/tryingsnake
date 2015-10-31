from distutils.core import setup

setup(
    name='tryingsnake',
    version='0.2.0',
    packages=['tryingsnake'],
    url='https://github.com/zero323/tryingsnake',
    license='MIT',
    author='Maciej Szymkiewicz',
    author_email='matthew.szymkiewicz@gmail.com',
    description='A simple, Scala inspired, Try implementation.',
    package_data={'tryingsnake': ['test/*.py']},
    zip_safe=False
)
