#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages
from tlclient.trader import __version__
import os

curr_dir = os.path.split(os.path.abspath(__file__))[0]
requirements = open(os.path.join(curr_dir, 'requirements.txt')).readlines()
requirements = [p.strip('\n') for p in requirements]
requirements = [p for p in requirements if p]
print(requirements)
print(__version__)

setup(
    name='tlclient',
    version=__version__,
    description=(
        'strategy side SDK for traders.link'
    ),
    long_description=open('README.rst').read(),
    author='puyuan.tech',
    author_email='info@puyuan.tech',
    maintainer='puyuan_staff',
    maintainer_email='github@puyuan.tech',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='http://docs.puyuan.tech',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=requirements,
)
