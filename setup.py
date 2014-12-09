import os
import re
from setuptools import setup
# parse version from package/module without importing or evaluating the code

with open('packer/__init__.py') as fh:
    for line in fh:
        m = re.search(r"^__version__ = '(?P<version>[^']+)'$", line)
    if m:
        version = m.group('version')
        break

setup(
    name = 'python-vagrant',
    version = version,
    license = 'MIT',
    description = 'Python bindings for creating Packer virtual machine images.',
    long_description = open(os.path.join(os.path.dirname(__file__),
                                         'README.md')).read(),
    keywords = 'python virtual machine image box packer virtualbox',
    url = 'https://github.com/kobe6661/python-packer',
    author = 'Konstantin Benz',
    author_email = 'konstantin.benz@gmail.com',
    classifiers = ['License :: OSI Approved :: MIT License',
                   'Development Status :: 4 - Beta',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   ],
    packages = ['packer'],
)