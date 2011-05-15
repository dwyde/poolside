import os
from subprocess import Popen, PIPE

def make_path(path_prefix, script):
    return os.path.join(*(path_prefix + [script]))

class Kernel(Popen):
    
    _ENCODING = 'utf-8'
    _TO_REPLACE = '\n'
    _DUMMY_CHAR = u'\uffff'
    
    def __init__(self, language, filename, preexec_fn=None):
        arg_list = [language, filename]
        Popen.__init__(self, arg_list, stdout=PIPE, stdin=PIPE,
                preexec_fn=preexec_fn)
    
    def send(self, message):
        command = self._encode(message)
        self.stdin.write('%s\n' % command)
    
    def recv(self):
        message = self.stdout.readline()[:-1]
        return self._decode(message)

    def _encode(self, message):
        command = message.replace('\n', self._DUMMY_CHAR)
        return command.encode(self._ENCODING)
    
    def _decode(self, message):
        command = message.decode(self._ENCODING)
        return command.replace(self._DUMMY_CHAR, '\n')
