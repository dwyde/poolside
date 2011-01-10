import tornado.httpserver
import tornado.ioloop
import tornado.websocket

import sys
import json
from optparse import OptionParser

import db_layer

from prep_kernel import interpreter
from multiprocessing import Process, Manager, Pipe

KERNEL_IP = '127.0.0.1'

import threading

class Responder(threading.Thread):
    def __init__(self, write_func, pipe_end):
        threading.Thread.__init__(self)
        self.write_func = write_func
        self.pipe_end = pipe_end
    
    def run(self):
        while True:
            message = self.pipe_end.recv()
            print message
            self.write_func(message)
    

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    managers = {}
    
    def __init__(self, application, request, server, db_port):
        tornado.websocket.WebSocketHandler.__init__(self, application, request)
        
        self.db = db_layer.Methods(server, db_port)
        
        self.dispatch = {
            'python': self.ipython_request,
            'save_worksheet': self.save_worksheet,
            'new_id': self.new_id,
            'delete_cell': self.delete_cell,
        }
    
    def open(self):
        manager = Manager()
        c, d = Pipe()
        
        kernel_p = Process(target=interpreter, args=(d,))
        kernel_p.start()
        
        self.managers[self] = c
        resp = Responder(self.write_message, c)
        resp.start()
        
    def on_message(self, message):
        #print message
        msg_dict = json.loads(message)
        self.dispatch[msg_dict['type']](msg_dict)

    def on_close(self):
        #kernel_p, conn = self.kernels[self.write_message]
        #conn.close()
        #kernel_p.terminate()
        pass
    
    def ipython_request(self, msg_dict):
        self.managers[self].send([msg_dict['input'], msg_dict['caller']])
        self.db.save_cell(msg_dict['caller'], 
                                   {'input': msg_dict['input'], 'output': ''})
        
    def save_worksheet(self, msg_dict):
        self.db.save_worksheet(msg_dict['id'], msg_dict['cells'])
    
    def new_id(self, msg_dict):
        cell_id = db_layer.new_id()
        self.db.save_cell(cell_id, {})
        self.write_message({'type': 'new_id', 'id': cell_id})
        
    def delete_cell(self, msg_dict):
        self.db.delete_cell(msg_dict['id']);

class ZMQApplication(tornado.web.Application):
    def __init__(self, server, db_port):
        handlers = [
            (r'/notebook', EchoWebSocket, dict(server=server, db_port=db_port)),
        ]
        tornado.web.Application.__init__(self, handlers)

def parse_arguments():
    parser = OptionParser()
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
    options = parse_arguments()
    application = ZMQApplication(options.couch_port, options.database)
    loop = tornado.ioloop.IOLoop.instance()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.ws_port)
    loop.start()

if __name__ == '__main__':
    main()
