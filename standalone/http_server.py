from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

import cgi
import json
import optparse
import sys
import os

from manager import KernelController

# Location of the file containing this server's address
ADDRESS_FILE = os.path.join('..', 'notebook', '_attachments', 'server.txt')
FALLBACK_ADDRESS = ('localhost', 8080)

# Global "controller" object
controller = KernelController()

class Handler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        if self.headers.get('Origin') != 'http://localhost:%d' % \
                self.server.couch_port:
            self.send_response(403, 'Bad "Origin" header')
            self.end_headers()
            return
        
        form = cgi.FieldStorage(fp=self.rfile,
            headers=self.headers, environ = {'REQUEST_METHOD':'POST'},
            keep_blank_values = 1)
        command = form.getvalue('content')
        worksheet_id = form.getvalue('worksheet_id')
        
        if command and worksheet_id:
            self.send_response(200)
            kernel = controller.get_or_create(worksheet_id)
            result = kernel.execute(command)
            message = json.dumps(result)
            self._respond(message)
        else:
            self.send_response(400, 'Parameters "content" and "worksheet_id" are \
required.')
            self._respond()
            
    def do_OPTIONS(self):
        self.send_response(200)
        self._respond()
        
    def _respond(self, message=None):
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:%d' %
                self.server.couch_port)
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Methods', 'OPTIONS, POST')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.end_headers()
        if message is not None:
            self.wfile.write(message)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

    def set_couch_port(self, couch_port):
        self.couch_port = couch_port

def parse_arguments():
    """Process command line arguments using :class:`optparse.OptionParser`.
    """
    
    parser = optparse.OptionParser()
    parser.add_option('-c', '--couch_port', dest='couch_port', default='5984', 
            metavar='COUCH_PORT', help='CouchDB server port (on localhost)', 
            type='int')

    (options, args) = parser.parse_args()
    
    del sys.argv[1:]
    
    return options

def read_address():
    address_text = open(ADDRESS_FILE, 'r').readline()
    address = address_text.split(':')
    return (address[0], int(address[1]))
        
def main():
    options = parse_arguments()
    address = read_address()
    server = ThreadedHTTPServer(address, Handler)
    server.set_couch_port(options.couch_port)
    print 'Starting server at %s.' % (address,)
    server.serve_forever()

if __name__ == '__main__':
    main()