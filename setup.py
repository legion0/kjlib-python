#!/usr/bin/env python
'''
Created on Feb 18, 2013

@author: legion
'''
from setuptools import setup
from kjlib import __version__

setup(
	name = "kjlib",
    version=__version__,
	description='Reusable Python Modules',
	packages=['kjlib'],
	url=r"https://github.com/legion0/kjlib-python",

	extras_require = {
		'jsbeautifier':  ["jsbeautifier"],
	},

	author='K Jonathan',
	author_email='phenixdoc@gmail.com',
)

