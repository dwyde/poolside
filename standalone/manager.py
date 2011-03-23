#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

from subprocess import Popen, PIPE
import threading

class Kernel:
    def __init__(self, **kwargs):
        #self.writers = set(kwargs['writers'])
        self.languages = set(['python', 'ruby'])
        self.python = Popen(['python', './pykernel.py'], stdout=PIPE,
                stdin=PIPE)
        self.ruby = Popen(['ruby', './rubykernel.rb'], stdout=PIPE, stdin=PIPE)
    
    def execute(self, language, command):
        if language in self.languages:
            kernel = getattr(self, language)
            sanitized = command.replace('\n', ' ')
            kernel.stdin.write('%s\n' % sanitized)
            result = kernel.stdout.readline()

            # This is a bit ugly: exec(), then eval() the result for JSON purposes
            try:
                content = eval(result)
            except Exception, error:
                content = result
        else:
            content = '<Bad language parameter in request>'
        
        return {
            'content': content,
            'type': 'output',
        }
    
    def terminate(self):
        self.python.stdin.close()
        self.python.stdout.close()
        self.python.terminate()

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
