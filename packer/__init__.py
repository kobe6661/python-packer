'''
Python bindings for working with Packer virtual machine image builder.
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

#log = logging.getLogger(__name__)

PACKER_NOT_FOUND_WARNING = 'The Packer executable cannot be found. ' \
                            'Please check if it is in the system path.'

def which(program):
    '''
    Emulate unix 'which' command. If program is a path to an executable file,
    returns program. Otherwise, if an executable file matching program is found in one
    of the directories in the PATH environment variable, return the first match
    found.
    On Windows, if PATHEXT is defined and program does not include an
    extension, include the extensions in PATHEXT when searching for a matching
    executable file.
    Return None if no executable file is found.
    http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python/377028#377028
    https://github.com/webcoyote/vagrant/blob/f70507062e3b30c00db1f0d8b90f9245c4c997d4/lib/vagrant/util/file_util.rb
    Python3.3+ implementation:
    https://hg.python.org/cpython/file/default/Lib/shutil.py
    '''

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    
    # Shortcut: If program contains any dir components, do not search the path
    # e.g. './backup', '/bin/ls'
    if os.path.dirname(program):
        if is_exe(program):
            return program
        else:
            return None
    
    # Are we on windows?
    # http://stackoverflow.com/questions/1325581/how-do-i-check-if-im-running-on-windows-in-python
    windows = (os.name == 'nt')
    # Or cygwin?
    # https://docs.python.org/2/library/sys.html#sys.platform
    cygwin = sys.platform.startswith('cygwin')
    
    # Paths: a list of directories
    path_str = os.environ.get('PATH', os.defpath)
    if not path_str:
        paths = []
    else:
        paths = path_str.split(os.pathsep)

    # The current directory takes precedence on Windows.
    if windows:
        paths.insert(0, os.curdir)
        # Only search PATH if there is one to search.
    if not paths:
        return None
    
    # Files: add any necessary extensions to program
    # On cygwin and non-windows systems do not add extensions when searching
    # for the executable
    if cygwin or not windows:
        files = [program]        
    else:
        # windows path extensions in PATHEXT.
        # e.g. ['.EXE', '.CMD', '.BAT']
        # http://environmentvariables.org/PathExt
        # This might not properly use extensions that have been "registered" in
        # Windows. In the future it might make sense to use one of the many
        # "which" packages on PyPI.
        exts = os.environ.get('PATHEXT', '').split(os.pathsep)
        # if the program ends with one of the extensions, only test that one.
        # otherwise test all the extensions.
        matching_exts = [ext for ext in exts if
                         program.lower().endswith(ext.lower())]
        if matching_exts:
            files = [program + ext for ext in matching_exts]
        else:
            files = [program + ext for ext in exts]

    # Check each combination of path, program, and extension, returning
    # the first combination that exists and is executable.
    for path in paths:
        for f in files:
            fpath = os.path.normcase(os.path.join(path, f))
            if is_exe(fpath):
                return fpath
    
    return None

# The full path to the vagrant executable, e.g. '/usr/bin/vagrant'
def get_packer_executable():
    return which('packer')
    
