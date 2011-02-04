from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

import cgi
import json

from manager import KernelController

controller = KernelController()

class Handler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:5984')
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

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main():
    server = ThreadedHTTPServer(('localhost', 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()

if __name__ == '__main__':
    main()