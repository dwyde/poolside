#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

"""Run an IPython kernel, customized with additional visualization features.
"""

import sys
import os
sys.path.append(os.path.join('..', 'visualize'))
from viz_extension import load_ipython_extension

from StringIO import StringIO

def Kernel(connection):
    globals_dict = {}
    locals_dict = {}
    load_ipython_extension(globals_dict)
    
    while True:
        command, caller = connection.recv()
        #code = compile(command, '<string>', 'exec')
        output_trap = StringIO()
        sys.stdout = output_trap
        try:
            exec command in globals_dict, locals_dict
        except Exception, error:
            sys.stdout.write('%s: %s' % (error.__class__.__name__, error))    
        result = output_trap.getvalue()
        
        message = {
            'content': result, 
            'target': caller,
            'type': 'output',
        }
        connection.send(message)

def interpreter(queue):
    """Set up an :class:`IPython.kernel.core.interpreter.Interpreter`.
    
    A kernel will listen for connections on a random local port.
    
    Each kernel's global namespace contains an instance of the 
    class :class:`visualize.dec.Viz`.  This variable `Viz` is callable::
        
        >>> a = range(5)
        >>> print Viz(a)
        ...
    
    Otherwise, this is a normal IPython interpreter.
    
    :param pipe: A :class:`multiprocessing.Connection` that enables \
    communication between this process and the main :class:`ws_tornado` server.
    """
    
    while True:
        message, caller = conn.recv()
        try:
            res = shell.execute(message)
        except Exception, error:
            res = {'stdout': '%s: %s' % (error.__class__.__name__, error)}
        conn.send({
            'content': res.get('stdout', ''), 
            'target': caller,
            'type': 'output',
        })

