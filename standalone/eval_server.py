from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn # switch to ForkingMixIn?
import argparse

import urllib2
import urllib

class EvalHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        print 'okay'
    
class EvalServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def read_arguments():
    '''Process command line arguments.'''
    
    parser = argparse.ArgumentParser(description='An HTTP server to run code')
    parser.add_argument('-p', '--port', type=int, required=True,
                       help='port on which the server will run', dest='port')

    args = parser.parse_args()
    return args


def main():
    args = read_arguments()
    address = ('127.0.0.1', args.port)
    server = EvalServer(address, EvalHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
    
