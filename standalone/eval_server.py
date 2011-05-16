from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import argparse
import cgi
import json
import urllib
import Cookie
import urllib2
import threading

from kernels import KernelController

# Parameters required in client POST requests
_REQUIRED_FIELDS = set(['worksheet', 'content', 'language'])

def parse_query(fh, length):
    query = cgi.FieldStorage(
                    fp=fh,
                    environ={
                             'REQUEST_METHOD':'POST', 
                             'CONTENT_LENGTH': length,
                             'CONTENT_TYPE': 'application/x-www-form-urlencoded'
                    }
    )
    return dict((x, query.getvalue(x)) for x in _REQUIRED_FIELDS)

class EvalHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        request = parse_query(self.rfile, self.headers['Content-Length'])
        
        # Check that all required parameters have a value
        if all(request.values()):
            self.send_response(200)
            self.end_headers()
            
            kernel = self.server.controller.get_or_create(request['worksheet'])
            result = kernel.evaluate(request)
            message = json.dumps(result)
            self.wfile.write(message)
        else:
            self.send_response(400, 'Please provide %s.' %
                                ", ".join(_REQUIRED_FIELDS))
            self.end_headers()
    
class CouchAuthHandler(EvalHandler):
    
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
        request = urllib2.Request(self.server.couch_server + self.session_endpoint)
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
        if worksheet_id not in self.kernels:
            self.lock.acquire()
            self.kernels[worksheet_id] = KernelController(**kwargs)
            self.lock.release()
        return self.kernels[worksheet_id]

class EvalServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    
    controller = KernelMapper()

def read_arguments():
    '''Process command line arguments.'''
    
    parser = argparse.ArgumentParser(description='An HTTP server to run code')
    parser.add_argument('-p', '--port', type=int, required=True,
                       help='port on which the server will run', dest='port')
    parser.add_argument('-c', '--couch', required=True,
                       help='address at which CouchDB is running', dest='couch')
    args = parser.parse_args()
    return args

def main():
    args = read_arguments()
    address = ('127.0.0.1', args.port)
    server = EvalServer(address, CouchAuthHandler)
    server.couch_server = args.couch
    print 'Ready to serve at ', server.server_address
    server.serve_forever()

if __name__ == '__main__':
    main()
