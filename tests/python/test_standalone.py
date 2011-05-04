import unittest
import os

import sys
sys.path.append(os.path.join('..', '..', 'standalone'))

import urllib2
import urllib

class TestConfigProcessor(unittest.TestCase):
    
    def setUp(self):
        # Port at which the test server will run, on localhost
        port = 8284
        self.url = 'http://localhost:%d' % (port,)
    
    def test_works(self):
        data = urllib.urlencode({'worksheet': 'abc123', 'extra': 'hello!'})
        conn = urllib2.urlopen(self.url, data)
        print conn.read()
    
if __name__ == '__main__':
    unittest.main()  
