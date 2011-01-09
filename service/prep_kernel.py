#!/usr/bin/env python

'''
Start an IPython ZMQ kernel, customized with an additional magic function.
Derived from IPython.zmq.ipkernel.main()
'''

import sys
sys.path.append('../visualize')

from IPython.kernel.core.interpreter import Interpreter

from viz_extension import load_ipython_extension

def interpreter(q, callback):
    shell = Interpreter()
    load_ipython_extension(shell.user_ns)
    while True:
        message = q.get()
        res = shell.execute(message)
        print res
        callback.test(res)
