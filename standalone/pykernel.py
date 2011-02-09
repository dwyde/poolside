#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

"""Run a Python "kernel", customized with additional visualization features.
"""

import sys
from StringIO import StringIO

def main():
    """Set up a rudimentary Python "kernel".
    
    Messages should be sent to `connection` as a 2-length list of the form
    ``[input_string, cell_uuid]``.
    
    Each kernel's `locals` namespace contains an instance of the 
    class :class:`visualize.dec.Viz`.  This variable `Viz` is callable::
    
    >>> a = range(5)
    >>> print Viz(a)
    ...
    
    :param connection: A :class:`multiprocessing.Connection` that enables \
    communication between this process and the main :class:`ws_tornado` server.
    """
    
    globals_dict = {}
    locals_dict = {}
    
    while True:
        command = sys.stdin.readline()
        if not command:
            break
            
        output_trap = StringIO()
        pipe_out = sys.stdout
        sys.stdout = output_trap
        
        try:
            exec command in globals_dict, locals_dict
        except Exception, error:
            sys.stdout.write('%s: %s' % (error.__class__.__name__, error))    
        result = output_trap.getvalue()
        
        sys.stdout = pipe_out
        sys.stdout.write(result)
        sys.stdout.flush()
        
if __name__ == '__main__':
    main()