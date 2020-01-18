# -*- coding: utf-8 -*-
from setuptools import setup


def get_version(fname='mccabe.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


setup(
    version=get_version(),
)
