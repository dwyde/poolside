from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

import cgi
import json
import optparse
import sys

from manager import KernelController

# Global "controller" object
controller = KernelController()

class Handler(BaseHTTPRequestHandler):
    
    def do_POST(self):
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
            self.end_headers()
            self.wfile.write(message)
        else:
            self.send_response(400, 'Parameters "content" and "worksheet_id" \
are required.')
            self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def parse_arguments():
    """Process command line arguments using :class:`optparse.OptionParser`.
    """
    
    parser = optparse.OptionParser()
    parser.add_option('-p', '--port', dest='port', 
            default=8282, metavar='PORT', type='int',
            help='The local port on which this server will run')

    (options, args) = parser.parse_args()
    
    del sys.argv[1:]
    
    return options
        
def main():
    options = parse_arguments()
    address = ('localhost', options.port)
    server = ThreadedHTTPServer(address, Handler)
    print 'Starting server at %s.' % (address,)
    server.serve_forever()

if __name__ == '__main__':
    main()