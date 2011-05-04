import unittest
import os

import sys
sys.path.append(os.path.join('..', '..', 'standalone'))
import eval_server

import StringIO

import urllib

class TestParseQuery(unittest.TestCase):
    
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

if __name__ == '__main__':
    unittest.main()  
