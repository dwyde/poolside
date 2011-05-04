import unittest
import os

import sys
sys.path.append(os.path.join('..', '..', 'standalone'))
import eval_server
import manager

import StringIO

import urllib

class TestEvalServer(unittest.TestCase):
    
    def test_parse_query(self):
        request = {'hello': 'world', 'worksheet': 'test1'}
        query = urllib.urlencode(request)
        fh = StringIO.StringIO(query)
        response = eval_server.parse_query(fh, len(query))
        fh.close()
        self.assertEqual(request.get('worksheet'), response.get('worksheet'))
        self.assertNotEqual(request.get('hello'), response.get('hello'))
        
    def test_command_line_args(self):
        port = 8284
        sys.argv = ['test', '-p', str(port)]
        args = eval_server.read_arguments()
        self.assertEqual(args.port, port)

class TestEvalManager(unittest.TestCase):
    def setUp(self):
        self.controller = manager.KernelController('../../standalone/jail/')
    
    def test_execute_code(self):
        request = dict(worksheet='test123', language='python',
                       content='print 2**3')
        kernel = self.controller.get_or_create(request['worksheet'])
        result = eval_server.exec_code(request, kernel)
        self.assertEqual(result['content'], 8)

if __name__ == '__main__':
    unittest.main()  
