#!/usr/bin/env python

'''
Start an IPython ZMQ kernel, customized with an additional magic function.
Derived from IPython.zmq.ipkernel.main()
'''

import sys
sys.path.append('../visualize')

from IPython.kernel.core.interpreter import Interpreter

from viz_extension import load_ipython_extension

from multiprocessing.connection import Listener

def interpreter(q):
    '''Set up an :class:`IPython.kernel.core.interpreter.Interpreter`.
    '''
    
    setup_ip = ('127.0.0.1', 0)
    listener = Listener(setup_ip)
    q.send(listener.address)
    
    shell = Interpreter()
    load_ipython_extension(shell.user_ns)
    
    conn = listener.accept()
    
    while True:
        message, caller = conn.recv()
        try:
            res = shell.execute(message)
        except Exception, e:
            res = {'stdout': '%s: %s' % (e.__class__.__name__, e)}
        conn.send({
            'content': res.get('stdout', ''), 
            'target': caller,
            'type': 'output',
        })
        
