import tornado.httpserver
import tornado.ioloop
import tornado.websocket

import json
import zmq
from zmq.eventloop import zmqstream

# ZMQ socket address constants
KERNEL_IP = '127.0.0.1'
XREQ_PORT = 5575
SUB_PORT = 5576

class IPythonRequest(dict):
    def __init__(self, code, caller):
        self['msg_type'] = 'execute_request'
        self['header'] = {'msg_id': caller}
        self['content'] = {'code': code, 'silent': False}

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, ports=(0, 0)):
        tornado.websocket.WebSocketHandler.__init__(self, application, request)
        self._make_msg_dict()
        self.dispatcher = ZMQDispatcher(ports)
    
    def open(self):
        self.dispatcher.sub_stream.on_recv(self.write_wrapper)
        self.dispatcher.req_stream.on_recv(self.write_wrapper)

    def on_message(self, message):
        msg = json.loads(message)
        #dispatch based on msg['lang']
        to_send = IPythonRequest(msg['code'], msg['caller'])
        self.dispatcher.request_socket.send_json(to_send)

    def on_close(self):
        print "WebSocket closed"
        
    def _make_msg_dict(self):
        self.msg_dict = {}
        # IPython
        self.msg_dict.update({
            'stream': lambda x: x['data'],
            'pyout': lambda x: x['data'],
            'pyerr': lambda x: x['ename'] + '<br />' + x['evalue'],
        })
        
    def write_wrapper(self, message_parts):
        for part in message_parts:
            msg = json.loads(part)
            msg_type = msg.get('msg_type')
            if msg_type in self.msg_dict:
                output = self.msg_dict[msg_type](msg['content'])
                result = {'output': output}
                result.update({'target': msg['parent_header']['msg_id']})
                print result
                self.write_message(result)
        

class ZMQApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/test', EchoWebSocket, dict(ports=(5575, 5576))),
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

class ZMQDispatcher:
    def __init__(self, ports):
        ctx = zmq.Context()
        self.request_socket = ctx.socket(zmq.XREQ)
        self.request_socket.connect('tcp://%s:%d' % (KERNEL_IP, ports[0]))
        self.sub_socket = ctx.socket(zmq.SUB)
        self.sub_socket.connect('tcp://%s:%d' % (KERNEL_IP, ports[1]))
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, '')
        
        self._make_streams()
    
    def _make_streams(self):
        loop = ZMQLoop.instance()
        self.sub_stream = zmqstream.ZMQStream(self.sub_socket, loop)
        self.req_stream = zmqstream.ZMQStream(self.request_socket, loop)

def main():
    application = ZMQApplication()
    loop = ZMQLoop.instance()
    http_server = tornado.httpserver.HTTPServer(application, io_loop=loop)
    http_server.listen(9996)
    loop.start()

if __name__ == '__main__':
    main()
