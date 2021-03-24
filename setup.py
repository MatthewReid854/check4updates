#!/usr/bin/env python

import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="check4updates",
    version="0.0.1",
    description="Check if an updated package is available and prompt your users to upgrade",
    author="Matthew Reid",
    author_email="alpha.reliability@gmail.com",
    license="MIT",
    url="https://github.com/MatthewReid854/check4updates",
    keywords=[
        "check",
        "auto",
        "automatic",
        "upgrade",
        "update",
        "updater",
        "upgrader",
        "package",
        "utility",
        "new",
        "release",
        "autoupgrade",
        "autoupdate",
        "prompt",
        "users",
        "developers",
        "interactive",
        "pip",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "requests>=2.24.0",
    ],
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*"]
    ),
)
