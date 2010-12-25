import tornado.httpserver
import tornado.ioloop
from tornado import websocket

import json
import zmq
from zmq.eventloop import zmqstream, ioloop, stack_context

# ZMQ socket address constants
KERNEL_IP = '127.0.0.1'
XREQ_PORT = 5575
SUB_PORT = 5576
ALT_XREQ = 5578
ALT_SUB = 5579

class EchoWebSocket(websocket.WebSocketHandler):
    def __init__(self, application, request, ports=(0, 0)):
        websocket.WebSocketHandler.__init__(self, application, request)
        self.dispatcher = ZMQDispatcher(ports)
    
    def write_wrapper(self, msg):
        print msg
        self.write_message(msg[0])
        
    def open(self):
        #print "WebSocket opened"
        self.dispatcher.sub_stream.on_recv(self.write_wrapper)
        self.dispatcher.req_stream.on_recv(self.write_wrapper)

    def on_message(self, message):
        msg = json.loads(message)
        self.dispatcher.request_socket.send_json(msg)

    def on_close(self):
        print "WebSocket closed"

class ZMQApplication(tornado.web.Application):
    def __init__(self, handlers, *args, **kwargs):
        tornado.web.Application.__init__(self, handlers, *args, **kwargs)

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
    handlers = [(r'/test', EchoWebSocket, dict(ports=(5575, 5576))),]
    application = ZMQApplication(handlers)
    loop = ZMQLoop.instance()
    http_server = tornado.httpserver.HTTPServer(application, io_loop=loop)
    http_server.listen(9996)
    loop.start()

if __name__ == '__main__':
    main()
