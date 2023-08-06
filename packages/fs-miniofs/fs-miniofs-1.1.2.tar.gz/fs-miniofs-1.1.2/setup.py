#!/usr/bin/env python

from setuptools import setup, find_packages

with open("fs_miniofs/_version.py") as f:
    exec(f.read())

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: System :: Filesystems",
]

with open("README.rst", "rt") as f:
    DESCRIPTION = f.read()

REQUIREMENTS = ["boto3~=1.9", "fs~=2.4", "six~=1.10"]

setup(
    name="fs-miniofs",
    author="Max Klein",
    classifiers=CLASSIFIERS,
    description="MinIO S3 filesystem for PyFilesystem2",
    install_requires=REQUIREMENTS,
    license="MIT",
    long_description=DESCRIPTION,
    long_description_content_type="text/x-rst",
    packages=find_packages(),
    keywords=["pyfilesystem", "MinIO", "s3"],
    platforms=["any"],
    test_suite="nose.collector",
    url="https://github.com/telamonian/miniofs",
    version=__version__,
    entry_points={"fs.opener": ["minio = fs_miniofs.opener:MINIOFSOpener"]},
)
