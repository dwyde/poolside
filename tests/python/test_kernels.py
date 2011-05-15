import unittest
import os

import sys
sys.path.append(os.path.join('..', '..', 'standalone'))

from kernels import Kernel, PythonKernel, RubyKernel


class TestKernel(unittest.TestCase):
    def setUp(self):
        path = ['..', '..', 'standalone', 'jail', 'kernels']
        kernel_dir = os.path.join(*path)
        self.python = PythonKernel(kernel_dir)
        self.ruby = RubyKernel(kernel_dir)
        self.kernels = [self.python, self.ruby]
    
    def test_base_class(self):
        kernel = Kernel()
        self.assertRaises(NotImplementedError, kernel.send, '')
        self.assertRaises(NotImplementedError, kernel.recv)
    
    def test_encode_message(self):
        message = 'a\nb c'
        for kernel in self.kernels:
            encoded = kernel._encode(message)
            self.assertEqual(encoded, u'a\uffffb c')
            
    def test_decode_message(self):
        message = u'while 1:\uffff  pass'
        for kernel in self.kernels:
            decoded = kernel._decode(message)
            self.assertEqual(decoded, 'while 1:\n  pass')
    
    def test_eval_python(self):
        self.python.send('print range(5)')
        result = self.python.recv()
        self.assertEqual(result, '[0, 1, 2, 3, 4]')

    def test_eval_ruby(self):
        self.ruby.send('puts 2 + 3')
        result = self.ruby.recv()
        self.assertEqual(result, '5')

if __name__ == '__main__':
    unittest.main()  
