#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

"""A threaded HTTP server for executing Python and Ruby code (in subprocesses).

TO-DO:

* Accept CouchDB server address as a command line arg.
"""

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

import urlparse
import json
import optparse
import sys
import Cookie
import httplib

from manager import KernelController

# Base URL of the proxy server
COUCH_SERVER = 'localhost:5984'

# CouchDB _session handler
SESSION_ENDPOINT = '/_session'

class BasicHandler(BaseHTTPRequestHandler):
    """Execute code received via GET, without CouchDB authentication."""
    
    # All parameters that we're expecting to be in the query string.
    required_fields = ['worksheet_id', 'content', 'language', 'callback']
    
    def do_GET(self):
        """Execute code from a GET request, if it has the proper parameters."""
    
        self.query_data = self._query_dict()
        
        # The query_data values are never integers, so 0 won't get filtered out.
        params = filter(None, self.query_data)
        if len(params) != len(self.required_fields):
            self._fail_and_respond()
        else:
            self._exec_and_respond()
    
    def _query_dict(self):
        """Return a dictionary of predefined query string parameters."""
        
        parsed = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed.query, strict_parsing=True)
        query_data = ((key, query.get(key)) for key in self.required_fields)
        return dict([(key, value[0]) for key, value in query_data])

    def _fail_and_respond(self):
        """Send an HTTP error message when a request parameter is missing."""
        
        self.send_response(400, 'Parameters "worksheet_id", "language", \
and "content" are required. You must also provide a jsonp callback function.')
        self.end_headers()
    
    def _exec_and_respond(self):
        """Execute code when the request looks okay."""
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/javascript')
        self.end_headers()
        
        worksheet = self.query_data['worksheet_id']
        kernel = self.server.controller.get_or_create(worksheet)
        result = kernel.execute(self.query_data['language'],
                                self.query_data['content'])
        message = json.dumps(result)
        self._output_message(message)
    
    def _output_message(self, message):
        """Respond to the client: call a JavaScript function via jsonp."""
        
        self.wfile.write('%s(%s)' % (self.query_data['callback'], message))

class AuthenticatedHandler(BasicHandler):
    """Check that a user is logged in with CouchDB."""
    
    def do_GET(self):
        user = self._authenticate()
        if user is None:
            self.send_response(401, 'Please log in')
            self.end_headers()
        else:
            BasicHandler.do_GET(self)

    def _authenticate(self):
        """Check a CouchDB authentication cookie."""
        
        cookie_str = self.headers.get('Cookie')
        if cookie_str is None:
            return None
        
        # Some cookie exists: check if it's the right one
        auth_cookie = Cookie.BaseCookie(cookie_str)
        session = auth_cookie.get('AuthSession')
        if session is None:
            return None
        
        # The request included a CouchDB session cookie: authenticate the user
        conn = httplib.HTTPConnection(COUCH_SERVER)
        headers = {'Cookie': cookie_str}
        conn.request('GET', SESSION_ENDPOINT, headers=headers)
        res = conn.getresponse().read()
        
        # Now, we try to read the userCtx (CouchDB authentication) object
        userCtx = json.loads(res).get('userCtx')
        if userCtx is None:
            return None
        return userCtx.get('name')
        
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    
    # Global "controller" object
    controller = KernelController()

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
    address = ('127.0.0.1', options.port)
    server = ThreadedHTTPServer(address, AuthenticatedHandler)
    print 'Starting server at %s.' % (address,)
    server.serve_forever()

if __name__ == '__main__':
    main()
