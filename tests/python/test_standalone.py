import unittest
import os

# The code that we are testing.
BASE_PATH = os.path.join('..', '..', 'standalone')

import sys
sys.path.append(BASE_PATH)
from subprocess import Popen
import urllib2

from eval_server import EvalServer, EvalHandler

import socket

class TestConfigProcessor(unittest.TestCase):
    
    def setUp(self):
        # Port at which the test server will run, on localhost
        self.port = 8284
        server_file = os.path.join(BASE_PATH, 'eval_server.py')
        self.server = Popen(['python', server_file, '-p', str(self.port)])
    
    def tearDown(self):
        self.server.terminate()
    
    def test_works(self):
        conn = urllib2.urlopen('http://localhost:%d' % (self.port))
        #print conn.read()
        print 3
    
if __name__ == '__main__':
    #unittest.main()
    server_address = ('127.0.0.1', 8284)
    client_address = ('127.0.0.1', 8285)
    server = EvalServer(server_address, EvalHandler)
    #request_address = ('127.0.0.1', 8285)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.connect(server_address)

    print dir(server)
    handler = EvalHandler(s, client_address, server)
    print dir(handler)
    
    #server.finish_request('', request_address)
    
