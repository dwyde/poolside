#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

from multiprocessing import Process, Pipe
import threading

from pykernel import interpreter

def _new_id():
    pass

class KernelResponder(threading.Thread):
    """Handle messages from a kernel process."""
    
    def __init__(self, connection, callback):
        threading.Thread.__init__(self)
        self.callback = callback
        self.connection = connection
    
    def run(self):
        """
        Receive messages read from a :class:`multiprocessing.Connection`.
        
        Stop when an IOError or EOFError occurs.
        """
        
        while True:
            try:
                message = self.connection.recv()
            except (IOError, EOFError):
                break
            self.callback(message)

class Kernel:
    def __init__(self, callback, **kwargs):
        #self.writers = set(kwargs['writers'])
        self._parent_conn, self._child_conn = Pipe()
        
        self.process = Process(target=interpreter, args=(self._child_conn,))
        self.process.start()
        
        self.responder = KernelResponder(self._parent_conn, callback)
        self.responder.start()
    
    def execute(self, command):
        self._parent_conn.send(command)
    
    def terminate(self):
        self.process.terminate()
        #self._parent_conn.close()
        #self._child_conn.close()

class KernelController:
    def __init__(self, callback):
        self.kernels = {}
        self.callback = callback
    
    def get_or_create(self, worksheet_id, **kwargs):
        if worksheet_id not in self.kernels:
            self.kernels[worksheet_id] = Kernel(self.callback, **kwargs)
        return self.kernels[worksheet_id]