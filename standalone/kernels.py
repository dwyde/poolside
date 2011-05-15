import os
from subprocess import Popen, PIPE

def make_path(path_prefix, script):
    return os.path.join(*(path_prefix + [script]))

class Kernel(Popen):
    
    def __init__(self, command, filename, preexec_fn=None):
        arg_list = [command, filename]
        Popen.__init__(self, arg_list, stdout=PIPE, stdin=PIPE,
                preexec_fn=preexec_fn)
    
    def send(self, message):
        self.stdin.write('%s\n' % message)
    
    def recv(self):
        return self.stdout.readline()[:-1]
