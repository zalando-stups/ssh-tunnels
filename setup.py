#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect

import setuptools
from setuptools import setup

__location__ = os.path.join(os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe())))


def read_version(package):
    data = {}
    with open(os.path.join(package, '__init__.py'), 'r') as fd:
        exec (fd.read(), data)
    return data['__version__']


NAME = 'stups-ssh-tunnels'
MAIN_PACKAGE = 'tunnels'
VERSION = read_version(MAIN_PACKAGE)
DESCRIPTION = 'Convenience tool to create SSH tunnels to cluster applications on AWS'
LICENSE = 'Apache License 2.0'
URL = 'https://github.com/zalando-stups/ssh-tunnels'
AUTHOR = 'Henning Jacobs'
EMAIL = 'henning.jacobs@zalando.de'

# Add here all kinds of additional classifiers as defined under
# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: CPython',
]

CONSOLE_SCRIPTS = ['tunnels = tunnels.cli:cli']


def get_install_requirements(path):
    content = open(os.path.join(__location__, path)).read()
    return [req for req in content.split('\\n') if req != '']


def read(fname):
    return open(os.path.join(__location__, fname), encoding='utf-8').read()


def setup_package():
    # Some helper variables
    version = VERSION

    install_reqs = get_install_requirements('requirements.txt')

    setup(
        name=NAME,
        version=version,
        url=URL,
        description=DESCRIPTION,
        author=AUTHOR,
        author_email=EMAIL,
        license=LICENSE,
        keywords='tunnels aws stups',
        packages=setuptools.find_packages(),
        long_description=read('README.rst'),
        install_requires=install_reqs,
        entry_points={'console_scripts': CONSOLE_SCRIPTS},
    )


if __name__ == '__main__':
    setup_package()
