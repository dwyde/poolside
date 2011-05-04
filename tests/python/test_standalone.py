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
        
#class TestConfigProcessor(unittest.TestCase):    

if __name__ == '__main__':
    unittest.main()  
