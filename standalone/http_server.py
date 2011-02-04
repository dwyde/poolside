from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

import cgi
import json

class Handler(BaseHTTPRequestHandler):
    
    #def do_GET(self):
    def do_POST(self):
        self.send_response(200)
        #self.send_header('Access-Control-Allow-Origin', 'http://localhost:5984')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        form = cgi.FieldStorage(fp=self.rfile,
            headers=self.headers, environ = {'REQUEST_METHOD':'POST'},
            keep_blank_values = 1)

        try:
            message = form['content'].value
        except KeyError:
            message = 'empty?'
        self.wfile.write(json.dumps({'content': message, 'type': 'output'}))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main():
    server = ThreadedHTTPServer(('localhost', 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()

if __name__ == '__main__':
    main()