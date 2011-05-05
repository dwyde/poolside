#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

from subprocess import Popen, PIPE
import threading
import resource
import ast
import os

_ENCODING = 'utf-8'
_DUMMY_CHAR = u'\uffff'

def respond(content, msg_type='output'):
    return {
        'content': content,
        'type': msg_type,
    }

def _setlimits(): # Should take in kwargs?
    """
    Set somewhat arbitrary limits on kernels' CPU time (seconds), child
    processes (number), and virtual memory (bytes).
    """
    
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    resource.setrlimit(resource.RLIMIT_NPROC, (2024, 2024))
    resource.setrlimit(resource.RLIMIT_AS, (500777216, 500777216))
    resource.setrlimit(resource.RLIMIT_NOFILE, (50, 50))

def exec_code(request, kernel):
    """Execute code when the request looks okay."""
    
    result = kernel.execute(request['language'], request['content'])
    return result

class Kernel:

    _kernel_map = {
        'python': 'code/kernels/pykernel.py',
        'ruby': 'code/kernels/rubykernel.rb',
    }

    def __init__(self, path_prefix='', **kwargs):
        #self.writers = set(kwargs['writers'])
        self.path_prefix = path_prefix
        self.languages = set(self._kernel_map.keys())
        for language in self.languages:
            kernel = self._make_kernel(language)
            setattr(self, language, kernel)
    
    def execute(self, language, command):
        if language in self.languages:
            kernel = getattr(self, language)
            sanitized = command.replace('\n', _DUMMY_CHAR).encode(_ENCODING)
            kernel.stdin.write('%s\n' % sanitized)
            
            # Get result, minus the added newline
            raw_result = kernel.stdout.readline()[:-1]
            result = raw_result.decode(_ENCODING).replace(_DUMMY_CHAR, '\n')

            # If possible, convert the output string (sent from a subprocess
            # kernel) into a Python object. Safer than "eval()".
            try:
                content = ast.literal_eval(result)
            except (SyntaxError, ValueError):
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
        path = os.path.join(self.path_prefix, filename)
        arg_list = [language, path]
        return Popen(arg_list, stdout=PIPE, stdin=PIPE, preexec_fn=_setlimits)

class KernelController:
    def __init__(self, kernel_path_prefix=''):
        self.kernels = {}
        self.lock = threading.Lock()
        self.path_prefix = kernel_path_prefix
    
    def get_or_create(self, worksheet_id, **kwargs):
        if worksheet_id not in self.kernels:
            self.lock.acquire()
            self.kernels[worksheet_id] = Kernel(self.path_prefix, **kwargs)
            self.lock.release()
        return self.kernels[worksheet_id]
