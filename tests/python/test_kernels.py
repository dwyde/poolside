"""Unit tests for the `kernels` module."""

import unittest
import os

import sys
sys.path.append(os.path.join('..', '..', 'standalone'))

from kernels import Kernel, KernelController, Message, respond

PATH = os.path.join('..', '..', 'standalone', 'jail', 'kernels')

def check_pid(pid):
    return os.path.exists('/proc/%d' % pid)

class TestKernel(unittest.TestCase):

    def setUp(self):
        self.python = Kernel('python', os.path.join(PATH, 'pykernel.py'))
        self.ruby = Kernel('ruby', os.path.join(PATH, 'rubykernel.rb'))
        self.kernels = [self.python, self.ruby]
    
    def tearDown(self):
        for kernel in self.kernels:
            kernel.terminate()
    
    def test_encode_message(self):
        message = 'a\nb c'
        for kernel in self.kernels:
            encoded = kernel._encode(message).decode(kernel._ENCODING)
            self.assertEqual(encoded, u'a\uffffb c')
            
    def test_decode_message(self):
        message = u'while 1:\n  pass'
        for kernel in self.kernels:
            encoded = message.encode(kernel._ENCODING)
            decoded = kernel._decode(encoded)
            self.assertEqual(decoded, message)
    
    def test_eval_python(self):
        self.python.send('print range(5)')
        result = self.python.recv()
        self.assertEqual(result, '[0, 1, 2, 3, 4]\n')

    def test_eval_ruby(self):
        self.ruby.send('puts 2 + 3')
        result = self.ruby.recv()
        self.assertEqual(result, '5\n')
    
    def test_eval_code(self):
        for kernel in self.kernels:
            result = kernel.eval_code('print 5+3')
            self.assertEqual(result, 8)

class TestKernelController(unittest.TestCase):
    def setUp(self):
        self.controller = KernelController(PATH)
    
    def tearDown(self):
        del self.controller
    
    def test_has_python(self):
        python = 'python' in self.controller
        self.assertEqual(python, True)
    
    def test_has_ruby(self):
        ruby = 'ruby' in self.controller
        self.assertEqual(ruby, True)
    
    def test_empty_language(self):
        empty = '' in self.controller
        self.assertEqual(empty, False)

    def test_delete_kernel(self):
        language = 'python'
        controller = KernelController(PATH)
        kernel = controller._get_kernel(language)
        pid = kernel.pid
        self.assertEqual(check_pid(pid), True)
        controller.delete_kernel(language)
        kernel.wait()
        self.assertEqual(check_pid(pid), False)
        self.assertEqual(language in controller, False)
    
    def test_delete_controller(self):
        """
        Check that deleting a controller will kill child subprocesses.
        """
        
        controller = KernelController(PATH)
        kernels = [controller._get_kernel(lang) \
                for lang in controller.languages()]
        pids = [kernel.pid for kernel in kernels]
        del controller
        for pid, kernel in zip(pids, kernels):
            kernel.wait()
            self.assertEquals(check_pid(pid), False)
        
    def test_evaluate(self):
        commands = {
            'python': ('print range(4)', [0, 1, 2, 3]),
            'ruby': ('puts 5+2', 7),
        }
        controller = KernelController(PATH)
        for language in controller.languages():
            code, expected = commands[language]
            message = Message(language=language, content=code)
            result = controller.evaluate(message)
            self.assertEquals(result, respond(expected))

if __name__ == '__main__':
    unittest.main()  
