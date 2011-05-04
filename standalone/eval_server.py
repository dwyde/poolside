from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn # switch to ForkingMixIn?
import argparse
import cgi
import json

import urllib2
import urllib


from manager import KernelController

REQUIRED_FIELDS = set(['worksheet', 'content', 'language'])

def parse_query(fh, length):
    query = cgi.FieldStorage(
                    fp=fh,
                    environ={
                             'REQUEST_METHOD':'POST', 
                             'CONTENT_LENGTH': length,
                             'CONTENT_TYPE': 'application/x-www-form-urlencoded'
                    }
    )
    return dict((x, query.getvalue(x)) for x in REQUIRED_FIELDS)

def exec_code(request, kernel):
    """Execute code when the request looks okay."""
    
    result = kernel.execute(request['language'], request['content'])
    return result

class EvalHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        request = parse_query(self.rfile, self.headers['Content-Length'])
        
        # Check that all required parameters have a value
        if all(request.values()):
            self.send_response(200)
            self.end_headers()
            
            kernel = self.server.controller.get_or_create(request['worksheet'])
            result = exec_code(request, kernel)
            message = json.dumps(result)
            self.wfile.write(message)
        else:
            self.send_response(400, 'Please provide %s.' %
                                "".join(REQUIRED_FIELDS))
            self.end_headers()
    
    
class EvalServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    
    controller = KernelController('jail/')

def read_arguments():
    '''Process command line arguments.'''
    
    parser = argparse.ArgumentParser(description='An HTTP server to run code')
    parser.add_argument('-p', '--port', type=int, required=True,
                       help='port on which the server will run', dest='port')

    args = parser.parse_args()
    return args


def main():
    args = read_arguments()
    address = ('127.0.0.1', args.port)
    server = EvalServer(address, EvalHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
    
