#!/usr/bin/env python
# 
# This file is part of Poolside, a computational notebook.
# Copyright (C) 2011 David Wyde and Chris Hart, New College of Florida
#
# Poolside is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 
# 02110-1301, USA.

"""
Run a Python "kernel", customized with additional visualization features.
"""

_ENCODING = 'utf-8'
_DUMMY_CHAR = u'\uffff'

import sys
from StringIO import StringIO

def main():
    """Set up a rudimentary Python "kernel"."""
    
    globals_dict = {}
    locals_dict = {}
    
    while True:
        raw_command = sys.stdin.readline()
        if not raw_command:
            break
        command = raw_command.decode(_ENCODING).replace(_DUMMY_CHAR, '\n')
            
        output_trap = StringIO()
        pipe_out = sys.stdout
        sys.stdout = output_trap
        
        try:
            exec command in globals_dict, locals_dict
        except Exception, error:
            sys.stdout.write('%s: %s' % (error.__class__.__name__, error))    
        result = output_trap.getvalue().replace('\n', _DUMMY_CHAR)
        
        sys.stdout = pipe_out
        sys.stdout.write(result.encode(_ENCODING) + '\n')
        sys.stdout.flush()
        
if __name__ == '__main__':
    main()
