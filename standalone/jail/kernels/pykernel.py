#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

"""Run a Python "kernel", customized with additional visualization features.
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
