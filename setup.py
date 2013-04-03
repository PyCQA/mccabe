# -*- coding: utf-8 -*-
from __future__ import with_statement
from setuptools import setup


def get_version(fname='mccabe.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in ('README.rst',):
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='mccabe',
    version=get_version(),
    description="McCabe checker, plugin for flake8",
    long_description=get_long_description(),
    keywords='flake8 mccabe',
    author='Tarek Ziade',
    author_email='tarek@ziade.org',
    maintainer='Florent Xicluna',
    maintainer_email='florent.xicluna@gmail.com',
    url='https://github.com/flintwork/mccabe',
    license='Expat license',
    py_modules=['mccabe'],
    zip_safe=False,
    entry_points={
        'flake8.extension': [
            'C90 = mccabe:McCabeChecker',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
