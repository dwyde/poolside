import unittest
import os
from urllib2 import urlopen

import sys
sys.path.append(os.path.join('..', '..', 'standalone'))
import eval_server
import config

class TestEvalServer(unittest.TestCase):
    
    def test_parse_query(self):
        result = urlopen(config.DEFAULT_PORT)
        
        
if __name__ == '__main__':
    unittest.main()  
