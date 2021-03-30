#!/usr/bin/env python

import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="check4updates",
    version="0.0.2",
    description="A library for Python developers that prompts your users to upgrade when a new version of your package is released",
    author="Matthew Reid",
    author_email="alpha.reliability@gmail.com",
    license="MIT",
    url="https://check4updates.readthedocs.io/en/latest/",
    project_urls={
        'Documentation': 'https://check4updates.readthedocs.io/en/latest/',
        'Source Code': 'https://github.com/MatthewReid854/check4updates',
    },
    keywords=[
        "check",
        "auto",
        "automatic",
        "upgrade",
        "update",
        "updates",
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
