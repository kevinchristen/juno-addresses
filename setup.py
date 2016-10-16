# Copyright 2016, Kevin Christen and the juno-addresses contributors.

from setuptools import setup, find_packages


setup(
    author="Kevin Christen",
    author_email="kevin.christen@gmail.com",
    entry_points={
        'console_scripts': ['juno2gmail = juno_addresses.gmail:main']
    },
    license="Apache License, Version 2.0",
    name="juno-addresses",
    packages=find_packages(),
    test_suite='tests',
    url="https://github.com/kevinchristen/juno-addresses",
    version="0.1",
 )
