#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

from multiprocessing import Process, Pipe
import threading

from pykernel import interpreter

class Kernel:
    def __init__(self, **kwargs):
        #self.writers = set(kwargs['writers'])
        self._parent_conn, self._child_conn = Pipe()
        
        self.process = Process(target=interpreter, args=(self._child_conn,))
        self.process.start()
    
    def execute(self, command):
        self._parent_conn.send(command)
        return self._parent_conn.recv()
    
    def terminate(self):
        self.process.terminate()
        #self._parent_conn.close()
        #self._child_conn.close()

class KernelController:
    def __init__(self):
        self.kernels = {}
        self.lock = threading.Lock()
    
    def get_or_create(self, worksheet_id, **kwargs):
        if worksheet_id not in self.kernels:
            self.lock.acquire()
            self.kernels[worksheet_id] = Kernel(**kwargs)
            self.lock.release()
        return self.kernels[worksheet_id]