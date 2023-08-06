#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

from tengu import __version__ as version

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
        'flask-sqlalchemy',
        'flask',
        'schedule',
        'uvicorn',
        'fastapi',
    ]

setup_requirements = []

test_requirements = [
        'tox',
    ]

setup(
    author="Barak Avrahami",
    author_email='barak1345@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Tengu is an OpenBalkans node implementation",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='tengu',
    name='tengu',
    packages=find_packages(include=['tengu']),
    python_requires='>=3',
    setup_requires=setup_requirements,
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'tengu-flask=tengu.cli:main_entrypoint',
            'tengu-fastapi=tengu.cli:fastapi_ep',
            ]
        },
    tests_require=test_requirements,
    url='https://github.com/openbalkans/tengu',
    version=version,
    zip_safe=False,
)
