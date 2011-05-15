import unittest
import os

import sys
sys.path.append(os.path.join('..', '..', 'standalone'))

from kernels import Kernel, make_path


class TestKernel(unittest.TestCase):

    def setUp(self):
        path = ['..', '..', 'standalone', 'jail', 'kernels']
        self.python = Kernel('python', make_path(path, 'pykernel.py'))
        self.ruby = Kernel('ruby', make_path(path, 'rubykernel.rb'))
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

if __name__ == '__main__':
    unittest.main()  
