import tornado.httpserver
import tornado.ioloop
import tornado.websocket

import json
import zmq
from zmq.eventloop import zmqstream

import db_layer

# ZMQ socket address constants
KERNEL_IP = '127.0.0.1'
XREQ_PORT = 5575
SUB_PORT = 5576

class ZMQReceiver:
    msg_dict = {
        'stream': lambda x: x['data'],
        'pyout': lambda x: x['data'],
        'pyerr': lambda x: x['ename'] + ': ' + x['evalue'],
    }
  
    def __init__(self, write_func, db):
        self.write_message = write_func
        self.db = db
  
    def __call__(self, message_parts):
        for part in message_parts:
            msg = json.loads(part)
            msg_type = msg.get('msg_type')
            if msg_type in self.msg_dict:
                output = self.msg_dict[msg_type](msg['content'])
                result = {
                    'type': 'output',
                    'content': output,
                    'target': msg['parent_header']['msg_id']
                }
                self.db.save_cell(result['target'], 
                                {'output': result['content']})
                self.write_message(result)

class IPythonRequest(dict):
    def __init__(self, code, caller):
        dict.__init__(self)
        self['msg_type'] = 'execute_request'
        self['header'] = {'msg_id': caller}
        self['content'] = {'code': code, 'silent': False}

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, ports=(0, 0)):
        tornado.websocket.WebSocketHandler.__init__(self, application, request)
        self.db = db_layer.Methods()
        self.receiver = ZMQReceiver(self.write_message, self.db)
        self.zmq_container = ZMQContainer(ports)
        self.dispatch = {
            'python': self.ipython_request,
            'save_worksheet': self.save_worksheet,
            'new_id': self.new_id,
            'delete_cell': self.delete_cell,
        }
        
    def open(self):
        self.zmq_container.sub_stream.on_recv(self.receiver)
        self.zmq_container.req_stream.on_recv(self.receiver)

    def on_message(self, message):
        msg_dict = json.loads(message)
        self.dispatch[msg_dict['type']](msg_dict)

    def on_close(self):
        pass
    
    def ipython_request(self, msg_dict):
        to_send = IPythonRequest(msg_dict['input'], msg_dict['caller'])
        self.zmq_container.request_socket.send_json(to_send)
        cell_id = self.db.save_cell(msg_dict['caller'], 
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
    def __init__(self):
        handlers = [
            (r'/notebook', EchoWebSocket, dict(ports=(XREQ_PORT, SUB_PORT))),
        ]
        settings = dict(
            cookie_secret="secret_ha$h",
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class ZMQLoop(tornado.ioloop.IOLoop):
    NONE = 0
    READ = zmq.POLLIN
    WRITE = zmq.POLLOUT
    ERROR = zmq.POLLERR
    
    def __init__(self, impl=None):
        tornado.ioloop.IOLoop.__init__(self, impl=zmq.Poller())

class ZMQContainer:
    def __init__(self, ports):
        ctx = zmq.Context()
        self.request_socket = ctx.socket(zmq.XREQ)
        self.request_socket.connect('tcp://%s:%d' % (KERNEL_IP, ports[0]))
        
        self.sub_socket = ctx.socket(zmq.SUB)
        self.sub_socket.connect('tcp://%s:%d' % (KERNEL_IP, ports[1]))
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, '')

        loop = ZMQLoop.instance()
        self.req_stream = zmqstream.ZMQStream(self.request_socket, loop)
        self.sub_stream = zmqstream.ZMQStream(self.sub_socket, loop)

def main():
    application = ZMQApplication()
    loop = ZMQLoop.instance()
    http_server = tornado.httpserver.HTTPServer(application, io_loop=loop)
    http_server.listen(9996)
    loop.start()

if __name__ == '__main__':
    main()
