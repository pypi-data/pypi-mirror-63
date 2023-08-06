#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

try:
    with open('requirements.txt') as requirements_file:
        requirements = requirements_file.read()
except FileNotFoundError:
    requirements = []

setup(
    author="Casey Vockrodt",
    author_email='casey.vockrodt@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'sgipupdate=sgipupdate.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    name='sgipupdate',
    packages=find_packages(include=['sgipupdate', 'sgipupdate.*']),
    test_suite='tests',
    url='https://github.com/cvockrodt/sgipupdate',
    version='0.1.0',
)
