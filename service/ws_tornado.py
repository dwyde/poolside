#!/usr/bin/env python
#
# Copyright 2011 David Wyde and Chris Hart.
#

"""Run a `Tornado <http://github.com/facebook/tornado>`_ server that 
accepts HTML5 WebSocket connections.
"""

import tornado.httpserver
import tornado.ioloop
import tornado.websocket

import sys
import json
import optparse

from multiprocessing import Process, Pipe
from multiprocessing.connection import Client
import threading

from pykernel import interpreter
import db_layer

class Responder(threading.Thread):
    """Receive messages from a kernel process and output them to the client.
    Writing to CouchDB blocks this WebSocket connection.
    """
    
    def __init__(self, write_func, pipe_end, database, lock):
        threading.Thread.__init__(self)
        self.write_func = write_func
        self.pipe_end = pipe_end
        self.database = database
        self.lock = lock
    
    def run(self):
        """
        Handle messages read from a :class:`multiprocessing.Connection`.
        
        Stop when an EOFError occurs.
        """
        
        while True:
            try:
                message = self.pipe_end.recv()
            except EOFError:
                break
            self.write_func(message)
            self.lock.acquire()
            self.database.save_cell(message['target'], 
                                {'output': message['content']})
            self.lock.release()
    

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    """
    A Tornado handler for connections to HTML5 WebSockets.
    """
    
    # Map each instance of this class to a two-tuple:
    # (A :class:`Process` running the associated Python kernel, 
    #  multiprocessing Connection to this kernel)
    kernels = {}
    
    def __init__(self, application, request, db_port, database):
        """Initialize a CouchDB object and a method dispatcher for each connection.
        
        **NOTE**: these variables should ideally be shared between instances.
        """
        
        tornado.websocket.WebSocketHandler.__init__(self, application, request)
        
        self.database = db_layer.Methods(db_port, database)
        
        self.dispatch = {
            'python': self._ipython_request,
            'save_worksheet': self._save_worksheet,
            'new_id': self._new_id,
            'delete_cell': self._delete_cell,
        }
        
        # A lock to prevent attempts at simultaneous writes to CouchDB.
        # There should be one of these per connected notebook.
        self.lock = threading.Lock()
    
    def open(self):
        """
        On connection from a browser:
        
        1. create a lock for this object writing to CouchDB
        2. make and start a 
        """
        
        parent_conn, child_conn = Pipe()
        
        kernel_p = Process(target=interpreter, args=(child_conn,))
        kernel_p.start()
        
        address = parent_conn.recv()
        conn = Client(address)
        
        resp = Responder(self.write_message, conn, self.database, self.lock)
        resp.start()
        
        self.kernels[self] = (kernel_p, conn)
        
    def on_message(self, message):
        """Receive and dispatch a message from the client side of a WebSocket.
        """
        
        msg_dict = json.loads(message)
        self.dispatch[msg_dict['type']](msg_dict)

    def on_close(self):
        """React to the closing of a WebSocket connection."""
        
        process, conn = self.kernels[self]
        conn.close()
        process.terminate()
    
    ### WEBSOCKET MESSAGE HANDLERS ###
    
    def _ipython_request(self, msg_dict):
        
        conn = self.kernels[self][1]
        conn.send([msg_dict['input'], msg_dict['caller']])
        
        self.lock.acquire()
        self.database.save_cell(msg_dict['caller'], {'input': 
                msg_dict['input'], 'output': ''})
        self.lock.release()
        
    def _save_worksheet(self, msg_dict):
        self.database.save_worksheet(msg_dict['id'], msg_dict['cells'])
    
    def _new_id(self, msg_dict):
        """Fulfill WebSocket requests for a new cell UUID.
        """
        
        cell_id = db_layer.new_id()
        self.database.save_cell(cell_id, {})
        self.write_message({'type': 'new_id', 'id': cell_id})
        
    def _delete_cell(self, msg_dict):
        self.database.delete_cell(msg_dict['id'])

class WebSocketApp(tornado.web.Application):
    """A Tornado application that accepts connections via WebSockets."""
    
    def __init__(self, db_port, database):
        handlers = [
            (r'/notebook', EchoWebSocket, dict(db_port=db_port, 
                    database=database)),
        ]
        tornado.web.Application.__init__(self, handlers)

def parse_arguments():
    """Process command line arguments using :class:`optparse.OptionParser`.
    """
    
    parser = optparse.OptionParser()
    parser.add_option('-w', '--ws_port', dest='ws_port', metavar='WEBSOCKET',
            help='port on which the WEBSOCKET server will run', default='9996',
            type='int')
    parser.add_option('-c', '--couch_port', dest='couch_port', default='5984', 
            metavar='COUCH_PORT', help='CouchDB server port (on localhost)', 
            type='int')
    parser.add_option('-d', '--database', dest='database', metavar='DATABASE',
            help='name of the CouchDB database', default='notebook')

    (options, args) = parser.parse_args()
    
    del sys.argv[1:]
    
    return options

def main():
    """The :mod:`ws_tornado` module's main entry point.
    """
    options = parse_arguments()
    application = WebSocketApp(options.couch_port, options.database)
    loop = tornado.ioloop.IOLoop.instance()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.ws_port)
    loop.start()

if __name__ == '__main__':
    main()
