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

from multiprocessing.connection import Listener

from IPython.kernel.core.interpreter import Interpreter

_SETUP_IP = ('127.0.0.1', 0)

def interpreter(pipe):
    """Set up an :class:`IPython.kernel.core.interpreter.Interpreter`.
    
    The kernel will listen for connections on a random local port.
    This process will communicate with the main WebSocket server via
    the `pipe` variable, a :class:`multiprocessing.Connection`.
    
    The kernel's global namespace contains an instance of the 
    class :class:`visualize.dec.Viz`.  This variable `Viz` is callable::
        
        >>> a = range(5)
        >>> print Viz(a)
        ...
    
    Otherwise, this is a normal IPython interpreter.
    """
    
    listener = Listener(_SETUP_IP)
    pipe.send(listener.address)
    
    shell = Interpreter()
    load_ipython_extension(shell.user_ns)
    
    conn = listener.accept()
    
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

