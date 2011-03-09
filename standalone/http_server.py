from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

import cgi
import json
import optparse
import sys
import Cookie
import httplib

from manager import KernelController

# Base URL of the proxy server
PROXY_SERVER = 'localhost'

# CouchDB _session handler
SESSION_ENDPOINT = '/session'

# Global "controller" object
controller = KernelController()

class BasicHandler(BaseHTTPRequestHandler):
    """Execute code received via POST, without CouchDB authentication."""
    
    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile,
            headers=self.headers, environ = {'REQUEST_METHOD':'POST'},
            keep_blank_values = 1)
        command = form.getvalue('content')
        worksheet_id = form.getvalue('worksheet_id')
        
        if command and worksheet_id:
            self.send_response(200)
            self.cors_okay()
            kernel = controller.get_or_create(worksheet_id)
            result = kernel.execute(command)
            message = json.dumps(result)
            self.end_headers()
            self.wfile.write(message)
        else:
            self.send_response(400, 'Parameters "content" and "worksheet_id" \
are required.')
            self.cors_okay()
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.cors_okay()
        self.end_headers()
    
    def cors_okay(self):
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:5984')
        self.send_header('Access-Control-Allow-Headers', 'x-requested-with')

class AuthenticatedHandler(BasicHandler):
    
    def do_POST(self):
        print dir(self)
        user = self._authenticate()
        if user is None:
            self.send_response(401, 'Please log in')
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
            self.end_headers()
            self.wfile.write(message)
        else:
            self.send_response(400, 'Parameters "content" and "worksheet_id" \
are required.')
            self.end_headers()

    def _authenticate(self):
        cookie_str = self.headers.get('Cookie')
        if cookie_str is None:
            return None
        print cookie_str
        
        # Some cookie exists: check if it's the right one
        auth_cookie = Cookie.BaseCookie(cookie_str)
        session = auth_cookie.get('AuthSession')
        if session is None:
            return None
        
        # The request included a CouchDB session cookie: authenticate the user
        conn = httplib.HTTPConnection(PROXY_SERVER)
        headers = {'Cookie': cookie_str}
        conn.request('GET', SESSION_ENDPOINT, headers=headers)
        res = conn.getresponse().read()
        
        # Now, we try to read the userCtx (CouchDB authentication) object
        userCtx = json.loads(res).get('userCtx')
        if userCtx is None:
            return None
        print userCtx
        return userCtx.get('name')
        
        

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
    server = ThreadedHTTPServer(address, BasicHandler)
    print 'Starting server at %s.' % (address,)
    server.serve_forever()

if __name__ == '__main__':
    main()
