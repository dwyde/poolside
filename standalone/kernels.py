import os
from subprocess import Popen, PIPE
import ast

def make_path(path_prefix, script):
    return os.path.join(*(path_prefix + [script]))

class Kernel(Popen):
    
    _ENCODING = 'utf-8'
    _TO_REPLACE = '\n'
    _DUMMY_CHAR = u'\uffff'
    
    def __init__(self, command, filename, preexec_fn=None):
        arg_list = [command, filename]
        Popen.__init__(self, arg_list, stdout=PIPE, stdin=PIPE,
                preexec_fn=preexec_fn)
    
    def send(self, message):
        """Encode and send a message to a kernel process."""
        
        command = self._encode(message)
        self.stdin.write('%s\n' % command)
    
    def recv(self):
        """Receive and decode a message from a kernel process.
        
        Block until a newline-terminated message is available.
        """
        
        message = self.stdout.readline()[:-1]
        return self._decode(message)

    def _encode(self, message):
        """Prepare a string of code for the kernel process."""
        
        command = message.replace(self._TO_REPLACE, self._DUMMY_CHAR)
        return command.encode(self._ENCODING)
    
    def _decode(self, message):
        """Prepare a kernel's message string for external use."""
        
        command = message.decode(self._ENCODING)
        return command.replace(self._DUMMY_CHAR, self._TO_REPLACE)

    def _eval_as_python(self, data_string):
        """Safely try to evaluate strings as builtin data types."""
        
        try:
            return ast.literal_eval(data_string)
        except (SyntaxError, ValueError):
            return data_string

    def eval_code(self, code):
        """Public method to evaluate code with this kernel."""
        
        self.send(code)
        result = self.recv()
        return self._eval_as_python(result)
