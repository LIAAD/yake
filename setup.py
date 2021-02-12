#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'tabulate',
    'click>=6.0',
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
    version='0.4.3',
    description="Keyword extraction Python package",
    long_description=readme,
    
    url='https://pypi.python.org/pypi/yake',
    packages=find_packages(include=['yake','StopwordsList']),
    entry_points={
        'console_scripts': [
            'yake=yake.cli:keywords'
        ]
    },
    license="LGPLv3",
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='yake',
    classifiers=[
classifiers=[
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
    ]
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
