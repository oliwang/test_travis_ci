#!/usr/bin/env python

from distutils.core import setup
from glob import glob
import os

from setuptools import find_packages

setup(name='Content_Extract',
      version='1.0',
      description='Extract content from url',
      author='Jiayi Wang',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')],
)
