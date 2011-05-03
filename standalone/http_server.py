#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

"""A threaded HTTP server for executing Python and Ruby code (in subprocesses).
"""

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

import urlparse
import json
import optparse # replace with argparse
import sys
import Cookie
import urllib2

from manager import KernelController
from setup_jail import setup_jail

# CouchDB _session handler
SESSION_ENDPOINT = '/_session'

class BasicHandler(BaseHTTPRequestHandler):
    """Execute code received via GET, without CouchDB authentication."""
    
    # All parameters that we're expecting to be in the query string.
    required_fields = ['worksheet_id', 'content', 'language', 'callback']
    
    def do_GET(self):
        """Execute code from a GET request, if it has the proper parameters."""
    
        self._process_input()
        params_okay = self._check_params()
        if params_okay:
            self._exec_and_respond()
        else:
            self._fail_and_respond()
    
    def _process_input(self):
        """Return a dictionary of predefined query string parameters."""
        
        parsed = urlparse.urlparse(self.path)
        query = urlparse.parse_qs(parsed.query, strict_parsing=True)
        query_data = ((key, query.get(key)) for key in self.required_fields)
        self.query_data = dict([(key, value[0]) for key, value in query_data])

    def _check_params(self):
        # The query_data values are never integers, so 0 won't get filtered out.
        params = filter(None, self.query_data)
        if len(params) != len(self.required_fields):
            return False
        else:
            self.callback = self.query_data['callback']
            return True

    def _fail_and_respond(self):
        """Send an HTTP error message when a request parameter is missing."""
        
        self.send_response(400, 'Parameters "worksheet_id", "language", \
and "content" are required. You must also provide a jsonp callback function.')
        self.end_headers()
    
    def _exec_and_respond(self):
        """Execute code when the request looks okay."""
        
        self._jsonp_okay()
        worksheet = self.query_data['worksheet_id']
        kernel = self.server.controller.get_or_create(worksheet)
        result = kernel.execute(self.query_data['language'],
                                self.query_data['content'])
        message = json.dumps(result)
        self._output_message(message)
    
    def _jsonp_okay(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/javascript')
        self.end_headers()
    
    def _output_message(self, message):
        """Respond to the client: call a JavaScript function via jsonp."""
        
        self.wfile.write('%s(%s)' % (self.callback, message))

class AuthenticatedHandler(BasicHandler):
    """Check that a user is logged in with CouchDB."""
    
    def do_GET(self):
        user = self._authenticate()
        if user is None:
            self._jsonp_okay()
            self._process_input()
            params_okay = self._check_params()
            if params_okay:
                self._output_message({'content': 'Please log in', 'type': 'error'})
            else:
                self._fail_and_respond()
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
        
        req = urllib2.Request(self.server.couch_server + SESSION_ENDPOINT)
        req.add_header('Cookie', cookie_str)
        res = urllib2.urlopen(req).read()
        
        # Now, we try to read the userCtx (CouchDB authentication) object
        userCtx = json.loads(res).get('userCtx')
        if userCtx is None:
            return None
        return userCtx.get('name')
        
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    
    # Global "controller" object
    controller = KernelController()
        
        
def _parse_arguments():
    """Process command line arguments using :class:`optparse.OptionParser`.
    """
    
    help_msg = 'URL of a config file attached to Poolside\'s design document.'
    parser = optparse.OptionParser()
    parser.add_option('-c', '--config_url', dest='config_url', help=help_msg)

    (options, args) = parser.parse_args()
    
    if not options.config_url:
        parser.error('Please specify the %s' % help_msg)
    
    return options

class ConfigProcessor:
    def __init__(self, config_url):
        self._url = config_url
        self._url_obj = urlparse.urlparse(config_url)
        
    def get_address(self):
        conn = urllib2.urlopen(self._url)
        response = conn.read()
        conn.close()
        info = json.loads(response)
        return (info['server'], info['port'])
    
    def get_server(self):
        return '%s://%s' % (self._url_obj.scheme, self._url_obj.netloc)

def main():
    # Process command line arguments
    options = _parse_arguments()
    config = ConfigProcessor(options.config_url)
    address = config.get_address()
    
    # Set up chroot jail
    setup_jail()
    
    # Create and run an HTTP Server
    server = ThreadedHTTPServer(address, AuthenticatedHandler)
    server.couch_server = config.get_server()
    print 'Starting server at %s.' % (address,)
    server.serve_forever()

if __name__ == '__main__':
    main()
