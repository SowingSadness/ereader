#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os

from setuptools import setup
#from setuptools.command.test import test as TestCommand


PACKAGE_NAME = 'ereader'


def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths, '': ['ereader.ini']}


setup(
    name=PACKAGE_NAME,
    version=get_version(PACKAGE_NAME),
    url='',
    license='BSD License',
    description='Effective Reader',
    long_description=open('README.rst').read(),
    author='unknown',
    author_email='unknown@mail',
    packages=get_packages(PACKAGE_NAME),
    package_data=get_package_data(PACKAGE_NAME),
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: Russian',
        'Intended Audience :: Developers',
    ],
    entry_points={'console_scripts': [
        'ereader = ereader.runner:main',
    ]},
    #install_requires=[
    #]
)
