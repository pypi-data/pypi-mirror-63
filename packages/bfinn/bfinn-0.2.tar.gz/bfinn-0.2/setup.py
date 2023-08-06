"""For packaging and installation."""

from setuptools import setup


setup(
    name='bfinn',
    packages=['bfinn'],
    version='0.2',
    author='Nicholas Georgescu',
    author_email='ngeorgescu@gmail.com',
    description='AFINN sentiment analysis with different english wordlist',
    license='Apache License 2.0',
    keywords='sentiment analysis',
    url='https://github.com/ngeorgescu/bfinn',
    package_data={'bfinn': ['data/*.txt', 'data/LICENSE']},
    long_description='',
    )
