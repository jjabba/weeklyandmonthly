# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="WeeklyAndMonthly",
    version="0.1.2",
    description="Calculate weekly and monthly averages from a set of datapoints.",
    license="MIT",
    author="Karl Berggren",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.9',
)
