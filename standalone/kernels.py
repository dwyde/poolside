import os
from subprocess import Popen, PIPE
import ast

# Mapping of the form {language: (command, script)}.
# If a system has two side-by-side Python installations, then specify
# the command to use in the first element on the value tuple.
_LANGUAGES = {
    'python': ('python', 'pykernel.py'),
    'ruby': ('ruby', 'rubykernel.rb'),
}

class KernelController(dict):
    """A class to wrap `Kernel`s for external use."""
    
    def __init__(self, path_prefix=''):
        """Class constructor: initialize kernels."""
        
        dict.__init__(self)
        
        for language, (command, script) in _LANGUAGES.iteritems():
            path = os.path.join(path_prefix, script)
            self._new_kernel(language, command, path)
    
    def _get_kernel(self, language):
        """Getter method for kernels."""
        
        return self.get(language)
    
    def _set_kernel(self, language, kernel):
        """Setter method for kernels."""
        
        self[language] = kernel
    
    def _new_kernel(self, language, command, path):
        """Create and assign a new kernel."""
        
        new_kernel = Kernel(command, path)
        self._set_kernel(language, new_kernel)
    
    def __del__(self):
        """Clean up on deletion of this controller."""
        
        for language, kernel in self.iteritems():
            kernel.terminate()
        #dict.__del__(self)
    
    def languages(self):
        """Return a list of kernel languages."""
        
        return self.keys()
    
    def delete_kernel(self, language):
        """Delete a kernel, and kill its underlying process."""
        
        kernel = self._get_kernel(language)
        kernel.terminate()
        del self[language]
    
    def evaluate(self, language, code):
        pass

class Kernel(Popen):
    """A process to execute code.
    
    The individual languages' kernel scripts are defined in external
    files.
    
    We need to reconcile our line buffering of the standard input and
    standard output streams with the significance of whitespace
    in Python. The current solution is to temporarily replace newline
    characters with a Unicode character reserved for internal use,
    send the data through the kernel process's standard input,
    then have the kernels do the opposite substitution (i.e., "put it
    back").
    """
    
    # String encoding to use for kernel messages.
    _ENCODING = 'utf-8'
    
    # Replace newlines.
    _TO_REPLACE = '\n'
    
    # Use a placeholder to reconcile line buffering with Python code.
    _DUMMY_CHAR = u'\uffff'
    
    def __init__(self, command, filename, preexec_fn=None):
        """Class constructor.
        
        :param command: A command to run, e.g., "python".
        :param filename: A script file to pass to the `command`.
        :param preexec_fn: A function to call in the child process.
        """
        
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
