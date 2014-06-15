# -*- coding: utf-8 -*-
from __future__ import with_statement
from setuptools import setup


def get_version():
    with open('wpadmin.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    with open('README.rst') as f:
        descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='wpadmin',
    version=get_version(),
    description="Command line tool for WordPress",
    long_description=get_long_description(),
    keywords='wordpress admin',
    author='Raul J. Chacon',
    author_email='raulchacon@outlook.com',
    url='https://github.com/raulchacon/wpadmin.py',
    license='MIT license',
    py_modules=['wpadmin'],
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'wpadmin = wpadmin:_main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License"
    ],
)
