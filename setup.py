# -*- coding: utf8 -*-
"""
A setuptools based setup module for ledger-bank-import project.

See:

* https://packaging.python.org/en/latest/distributing.html
* https://github.com/pypa/sampleproject
"""


from setuptools import setup, find_packages
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))


# get the long description from the README file
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ledgerbankimport',
    version='0.0.1.dev1',
    description='ledger-cli import scripts for various czech banks',
    long_description=long_description,
    url='http://github.com/mbukatov/ledger-bank-import/',
    author='Martin Bukatovič',
    author_email='martin.bukatovic@gmail.com',
    license='GPLv3',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Topic :: Utilities',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        ],
    packages=find_packages(exclude=['doc']),
    install_requires=[],
    # TODO: make this work with git (and remove MANIFEST.in?)
    # setup_requires=['setuptools_scm'],
    # use_scm_version=True,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ledger-bank-import=ledgerbankimport.main:main',
        ],
    },
    test_suite = 'ledgerbankimport.tests',
    )
