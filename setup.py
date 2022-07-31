#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from jsontp.__init__ import __version__

setup(
  name='jsontp',
  version=__version__,
  description='JSON Tree Parser',
  author='Nodiru Gaji',
  author_email='c0d3r.nodiru.gaji@gmail.com',
  url='https://github.com/ames0k0/jsontree',
  packages=['jsontp'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
  ]
)
