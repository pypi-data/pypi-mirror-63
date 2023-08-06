from __future__ import print_function
from setuptools import setup, find_packages
import pytools

with open("README.txt", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="pytoolstest",
    version=pytools.__version__,
    author="BobLiang",
    author_email="1591609343@qq.com",
    description="free python tools",
    long_description=long_description,
    license="MIT",
    url="https://www.cnblogs.com/7-pjk/",
    packages=find_packages(),
    install_requires=[
        "pygame <= 1.9.5",
        "requests"
        ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
