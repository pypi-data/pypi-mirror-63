#!/usr/bin/env python

"""
distutils/setuptools install script.
"""
import os
import re

import setuptools

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = ['requests', 'beautifulsoup4', 'tqdm', 'lxml']


def get_version():
    init = open(os.path.join(ROOT, 'src/sk', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setuptools.setup(
    name="skoy",  # Replace with your own username, default nomenclature is, {example-pkg}-{username}
    version=get_version(),
    author="Bruno Gomes",
    author_email="bgomes@youongroup.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    package_dir={"": "src"},
    install_requires=requires,
    scripts=[],
    packages=setuptools.find_namespace_packages(where="src", exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    entry_points={
        'console_scripts': [
            'sk = sk.package.__main__:main'
        ]
    },
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
