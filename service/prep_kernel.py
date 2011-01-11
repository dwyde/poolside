#!/usr/bin/env python

'''
Start an IPython ZMQ kernel, customized with an additional magic function.
Derived from IPython.zmq.ipkernel.main()
'''

import sys
sys.path.append('../visualize')

from IPython.kernel.core.interpreter import Interpreter

from viz_extension import load_ipython_extension

def interpreter(q):
    shell = Interpreter()
    load_ipython_extension(shell.user_ns)
    while True:
        message, caller = q.recv()
        try:
            res = shell.execute(message)
        except Exception, e:
            res = {'stdout': '%s: %s' % (e.__class__.__name__, e)}
        q.send({
            'content': res.get('stdout', ''), 
            'target': caller,
            'type': 'output',
        })
