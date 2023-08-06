#!/usr/bin/env python

from setuptools import find_namespace_packages, setup

setup(
    name="nomnomdata-auth",
    version="0.0.1",
    packages=find_namespace_packages(),
    description="Requests authorizer for HMAC signed payloads",
    author="Nom Nom Data Inc",
    author_email="info@nomnomdata.com",
    classifiers=["Programming Language :: Python :: 3.7"],
    include_package_data=True,
    zip_safe=False,
    install_requires=["requests"],
    entry_points={},
    python_requires=">=3.7",
)
