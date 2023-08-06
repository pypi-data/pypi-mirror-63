#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
import re
import codecs
import os

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0', 'autoflake>=1.2', 'flake8>=3.5.0', 'pytest>=3.6.2',
    'twine>=1.11.0', 'yapf>=0.22.0', 'Flask==1.0.2', 'Flask-Dropzone==1.5.3'
]

setup_requirements = []

test_requirements = []

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_pakcage_info(info, *file_paths):
    info_file = read(*file_paths)

    match = re.search(r"^__" + re.escape(info) + r"__ = ['\"]([^'\"]*)['\"]",
                      info_file, re.M)

    if match:
        return match.group(1)
    raise RuntimeError("Unable to find {} string.".format(info))


setup(
    author=find_pakcage_info('author', 'src', 'udserver', '__init__.py'),
    author_email=find_pakcage_info('email', 'src', 'udserver', '__init__.py'),
    version=find_pakcage_info('version', 'src', 'udserver', '__init__.py'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        exclude=["contrib", "docs", "tests*", "tasks", "udserver/storage/*"],
    ),
    # package_data={'yourpackage': ['*.txt', 'path/to/resources/*.txt']},
    description=
    "(udserver) a simple upload and download server, just for temporary file transfer. No security ensurance.",
    entry_points={
        'console_scripts': [
            'udserver=udserver.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='udserver',
    name='udserver',
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kedpter/udserver',
)
