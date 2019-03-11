#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'tabulate',
    'Click>=6.0',
    "numpy",
    "segtok",
    "networkx",
    "jellyfish"]

setup_requirements = [
    'pytest-runner'    
]

test_requirements = [
    "pytest",
    "flake8"
]

setup(
    name='yake',
    version='0.4.0',
    description="Keyword extraction Python package",
    long_description=readme,
    
    url='https://pypi.python.org/pypi/yake',
    packages=find_packages(include=['yake','StopwordsList']),
    entry_points={
        'console_scripts': [
            'yake=yake.cli:keywords'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='yake',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
