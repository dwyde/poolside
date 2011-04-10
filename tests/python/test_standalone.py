import unittest

import sys
sys.path.append('../../standalone')
import http_server

import urllib2

class TestConfigProcessor(unittest.TestCase):

    def test_good_config(self):
        config = http_server.ConfigProcessor('file:data/eval_server.json')
        address = config.get_address()
        self.assertEqual(address, ('localhost', 8283))
        
    def test_empty_config(self):
        config = http_server.ConfigProcessor('file:data/empty_config.json')
        self.assertRaises(ValueError, config.get_address)
    
    def test_missing_config(self):
        config = http_server.ConfigProcessor('file:xxx/yyy.zzz')
        self.assertRaises(urllib2.URLError, config.get_address)
    
    def test_good_server(self):
        config = http_server.ConfigProcessor('http://localhost:5984/config')
        server = config.get_server()
        self.assertEqual(server, 'localhost:5984')

if __name__ == '__main__':
    unittest.main()
