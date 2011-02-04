from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

import cgi
import json

import cgitb
cgitb.enable()

class Handler(BaseHTTPRequestHandler):
    
    #def do_GET(self):
    def do_POST(self):
        self.send_response(200)
        #self.send_header('Access-Control-Allow-Origin', 'http://localhost:5984')
        self.send_header('Access-Control-Allow-Origin', '*')
        #self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        
        #print self.rfile.readline()
        
        #form = cgi.FieldStorage(
        #    fp=self.rfile,
        #)
        form = cgi.FieldStorage(fp=self.rfile,
            headers=self.headers, environ = {'REQUEST_METHOD':'POST'},
            keep_blank_values = 1)
        
        #print form.keys()
        #form = {}
        ##received = self.rfile.read()
        #try:
        #    data = json.loads(self.rfile.read())
        #except Exception, error:
        #    print error
        #    message = 'hello!'
        #finally:
        #    print 'yes'
        #    message = data.get('content', '???')
        #message = self.rfile.read()
        try:
            message = form['content'].value
        except KeyError:
            message = 'empty?'
        self.wfile.write(json.dumps({'content': message, 'type': 'output'}))
        #self.wfile.write('\n')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main():
    server = ThreadedHTTPServer(('localhost', 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()

if __name__ == '__main__':
    main()