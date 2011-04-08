#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

from subprocess import Popen, PIPE
import threading
import resource

_ENCODING = 'utf-8'
_DUMMY_CHAR = u'\uffff'

def respond(content, msg_type='output'):
    return {
        'content': content,
        'type': msg_type,
    }

def _setlimits():
    # Set maximum CPU time to 1 second in child process, after fork() but before exec()
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))

class Kernel:

    _kernel_map = {
        'python': './pykernel.py',
        'ruby': './rubykernel.rb',
    }

    def __init__(self, **kwargs):
        #self.writers = set(kwargs['writers'])
        self.languages = set(self._kernel_map.keys())
        for language in self.languages:
            kernel = self._make_kernel(language)
            setattr(self, language, kernel)
    
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
            
            if kernel.poll() is not None:
                # Kernel process has terminated.
                new_kernel = self._make_kernel(language)
                setattr(self, language, new_kernel)
                content = '<Kernel died>'
        else:
            content = '<Bad language parameter in request>'
        
        return respond(content)
    
    def terminate(self):
        self.python.stdin.close()
        self.python.stdout.close()
        self.python.terminate()
        
    def _make_kernel(self, language):
        filename = self._kernel_map[language]
        arg_list = [language, filename]
        return Popen(arg_list, stdout=PIPE, stdin=PIPE, preexec_fn=_setlimits)

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
