"""Run an IPython kernel, customized with additional visualization features.
"""

import sys
sys.path.append('../visualize')
from viz_extension import load_ipython_extension

from multiprocessing.connection import Listener

from IPython.kernel.core.interpreter import Interpreter

_SETUP_IP = ('127.0.0.1', 0)

def interpreter(q):
    """Set up an :class:`IPython.kernel.core.interpreter.Interpreter`.
    """
    
    listener = Listener(_SETUP_IP)
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
        
