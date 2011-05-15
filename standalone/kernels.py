import os
from subprocess import Popen, PIPE

def make_path(path_prefix, script):
    return os.path.join(*(path_prefix + [script]))

class Kernel(Popen):
    
    _DUMMY_CHAR = u'\uffff'
    
    def __init__(self, language, filename, preexec_fn=None):
        arg_list = [language, filename]
        Popen.__init__(self, arg_list, stdout=PIPE, stdin=PIPE,
                preexec_fn=preexec_fn)
    
    def send(self, message):
        self.stdin.write('%s\n' % message)
    
    def recv(self):
        return self.stdout.readline()[:-1]

    def _encode(self, message):
        return message.replace('\n', self._DUMMY_CHAR)#.encode(_ENCODING)
    
    def _decode(self, message):
        return message.replace(self._DUMMY_CHAR, '\n')
