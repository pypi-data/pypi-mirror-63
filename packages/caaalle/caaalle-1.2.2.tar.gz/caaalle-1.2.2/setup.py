#!/usr/bin/env python3

import codecs
import os
import re
from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

_title = 'caaalle'
_description = 'caaalle'
_author = 'Carl Larsson'
_author_email = 'example@gmail.com'
_license = 'Apache 2.0'
_url = 'https://github.com/caalle/caaalle'

setup(
    name=_title,
    description=_description,
    long_description=readme,
    long_description_content_type='text/markdown',
    version=find_version("caaalle", "__init__.py"),
    author=_author,
    author_email=_author_email,
    url=_url,
    packages=['caaalle'],
    include_package_data=True,
    python_requires=">=3.8.*",
    install_requires=[],
    license=_license,
    zip_safe=False,
    entry_points={
        'caaalle': ['caaalle=caaalle.entry_points:main'],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='caaalle'
)
