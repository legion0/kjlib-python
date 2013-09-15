#!/usr/bin/env python

from distutils.core import setup
from kjlib import __version__

setup(name='kjlib',
      version=__version__,
      description='Reusable Python Modules',
      author='K Jonathan',
      author_email='phenixdoc@gmail.com',
      packages=['kjlib'],
	  url=r"https://github.com/legion0/kjlib-python"
     )
