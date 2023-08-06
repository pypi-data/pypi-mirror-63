# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read().strip()

install_requires = [
    'requests',
    'pyjwt'
]

tests_require = [
    'pyyaml',
    'pytest',
    'pytest-variables',
    'pytest-variables[yaml]'
]

setup(
    name='minerva-py',
    version='0.0.1',
    author='Lingfei Hu',
    author_email='hulingfei84@gmail.com',
    description='Python client for Minerva',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MarkDevTeamMgt/minerva-py',
    license='Apache License, Version 2.0',
    packages=find_packages(
        where='.',
        exclude=('tests*', )
    ),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=install_requires,

    test_suite='tests.run_tests.run_all',
    tests_require=tests_require,
)
