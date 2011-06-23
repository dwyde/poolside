#!/usr/bin/env python
# 
# This file is part of Poolside, a computational notebook.
# Copyright (C) 2011 David Wyde and Chris Hart, New College of Florida
#
# Poolside is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 
# 02110-1301, USA.

"""
Run an HTTP server to evaluate users' code.
"""

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import argparse
import cgi
import json
import Cookie
import urllib2
import threading

from kernels import KernelController

class EvalHandler(BaseHTTPRequestHandler):
    """Evaluate user code, via HTTP requests."""
    
    # Parameters required in client POST requests
    REQUIRED_FIELDS = set(['worksheet', 'content', 'language'])
    
    def do_POST(self):
        data = self._parse_query(self.rfile,
                                self.headers['Content-Length'])
        
        # Check that all required parameters have a value
        if all(data.values()):
            self.send_response(200)
            self.end_headers()
            
            kernel = self.server.mapper.get_or_create(data['worksheet'])
            result = kernel.evaluate(data)
            message = json.dumps(result)
            self.wfile.write(message)
        else:
            self.send_response(400, 'Please provide %s.' %
                                ", ".join(self.REQUIRED_FIELDS))
            self.end_headers()
    
    def _parse_query(self, file_handle, length):
        """Parse POST data into a dictionary."""
        
        data = cgi.FieldStorage(
                fp=file_handle,
                environ={
                     'REQUEST_METHOD':'POST', 
                     'CONTENT_LENGTH': length,
                     'CONTENT_TYPE': 'application/x-www-form-urlencoded'
                }
        )
        return dict((x, data.getvalue(x)) for x in self.REQUIRED_FIELDS)
    
class CouchAuthHandler(EvalHandler):
    """Authenticate users against CouchDB before evaluating code."""
    
    session_endpoint = '/_session'
    
    def do_POST(self):
        logged_in = self._authenticate()
        if logged_in:
            EvalHandler.do_POST(self)
        else:
            self.send_response(401, 'Please log in to CouchDB')
            self.end_headers()
        
    def _authenticate(self):
        """Check a CouchDB authentication cookie."""
        
        cookie_str = self.headers.get('Cookie')
        auth_cookie = Cookie.BaseCookie(cookie_str)
        session = auth_cookie.get('AuthSession')
        if session is None:
            return None
        
        # Check that a purported CouchDB authentication cookie is valid
        request = urllib2.Request(self.server.couch_server +
                self.session_endpoint)
        request.add_header('Cookie', cookie_str)
        conn = urllib2.urlopen(request)
        response = conn.read()
        conn.close()
        
        # Now, we try to read the userCtx (CouchDB authentication) object
        userCtx = json.loads(response).get('userCtx')
        if userCtx is None:
            return None
        else:
            return userCtx.get('name')

class KernelMapper:
    """
    Map worksheet ID's to kernels.
    
    There can be many readers, but there is a thread lock to write.
    """
    
    def __init__(self):
        """Class constructor."""
        
        self.kernels = {}
        self.lock = threading.Lock()
    
    def get_or_create(self, worksheet_id, **kwargs):
        """Return existing kernels and create nonexistent ones."""
        
        if worksheet_id not in self.kernels:
            self.lock.acquire()
            self.kernels[worksheet_id] = KernelController(**kwargs)
            self.lock.release()
        return self.kernels[worksheet_id]

class EvalServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    
    # An object to manage kernels.
    mapper = KernelMapper()
    
    # A CouchDB server's URL
    couch_server = None
    
    def set_couch_server(self, address):
        """Store a CouchDB URL, for later queries (authentication)."""
        
        self.couch_server = address

def read_arguments():
    """Process command line arguments."""
    
    parser = argparse.ArgumentParser(description='An HTTP server to run code')
    parser.add_argument('-p', '--port', type=int, required=True,
                       help='port on which the server will run', dest='port')
    parser.add_argument('-c', '--couch', required=True,
                       help='address at which CouchDB is running', dest='couch')
    args = parser.parse_args()
    return args

def main():
    """Main function: create and run an `EvalServer`."""
    args = read_arguments()
    address = ('127.0.0.1', args.port)
    server = EvalServer(address, EvalHandler)
    server.set_couch_server(args.couch)
    print 'Ready to serve at ', server.server_address
    server.serve_forever()

if __name__ == '__main__':
    main()
