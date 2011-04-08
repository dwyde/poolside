#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

from subprocess import Popen, PIPE
import threading

_ENCODING = 'utf-8'
_DUMMY_CHAR = u'\uffff'

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
            sanitized = command.replace('\n', _DUMMY_CHAR).encode(_ENCODING)
            kernel.stdin.write('%s\n' % sanitized)
            raw_result = kernel.stdout.readline()
            result = raw_result.decode(_ENCODING).replace(_DUMMY_CHAR, '\n')

            # This is a bit ugly: exec(), then eval() the result.
            # Do this to properly parse strings into JSON objects, but it
            # also results in things like "print 5 + 5\n" turning into "10".
            # Not sure how to handle this issue.
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
