from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

import cgi
import json
import optparse
import sys

from manager import KernelController

controller = KernelController()

class Handler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:%d' %
                self.server.couch_port)
        #self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        form = cgi.FieldStorage(fp=self.rfile,
            headers=self.headers, environ = {'REQUEST_METHOD':'POST'},
            keep_blank_values = 1)

        try:
            command = form['content'].value
            worksheet_id = form['worksheet_id'].value
        except KeyError:
            self.wfile.write('Parameters "content" and "worksheet_id" are \
required for Python requests.')
            #respond({'error': }, code=400)
        finally:
            kernel = controller.get_or_create(worksheet_id)
            message = kernel.execute(command)
            self.wfile.write(json.dumps(message))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:%d' %
                self.server.couch_port)
        #self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

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
    parser.add_option('-s', '--service_port', dest='service_port', metavar='SERVICE_PORT',
            help='port on which this HTTP server runs', default=8080, type='int')

    (options, args) = parser.parse_args()
    
    del sys.argv[1:]
    
    return options

def main():
    options = parse_arguments()
    server = ThreadedHTTPServer(('localhost', options.service_port), Handler)
    server.set_couch_port(options.couch_port)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()

if __name__ == '__main__':
    main()