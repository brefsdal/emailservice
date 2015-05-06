#!/usr/bin/env python

try:
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

version = "0.0.1"
setup(
    name="emailservice",
    version=version,
    packages=[
        "emailservice",
        "emailservice.mailgunapi",
        "emailservice.mandrillapi",
        "emailservice.test"
        ],
    package_dir={"emailservice": "emailservice"},
    package_data={"emailservice": ["emailservice.cfg"]},
    author="Brian Refsdal",
    author_email="brian.refsdal@gmail.com"
)