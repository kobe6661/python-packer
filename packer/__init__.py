'''
Python bindings for working with Vagrant and Vagrantfiles. Do useful things
with the `vagrant` CLI without the boilerplate (and errors) of calling
`vagrant` and parsing the results.
The API attempts to conform closely to the API of the `vagrant` command line,
including method names and parameter names.
Documentation of usage, testing, installation, etc., can be found at
https://github.com/todddeluca/python-vagrant.
'''

import collections
import os
import re
import subprocess
import sys
import logging

# python package version
# should match r"^__version__ = '(?P<version>[^']+)'$" for setup.py
__version__ = '0.0.1'