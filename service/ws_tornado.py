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

class EchoWebSocket(websocket.WebSocketHandler):
    def __init__(self, application, request, dispatcher=None):
        websocket.WebSocketHandler.__init__(self, application, request)
        
        dispatcher.sub_stream.on_recv(self.write_wrapper)
        dispatcher.req_stream.on_recv(self.write_wrapper)
        self.dispatcher = dispatcher
    
    def write_wrapper(self, msg):
        self.write_message(msg[0])
    
    #def initialize(self, dispatcher):
    #    #self.dispatcher = dispatcher
    #    dispatcher.sub_stream.on_recv(self.write_message)
    #    dispatcher.req_stream.on_recv(self.write_message)
    
    def open(self):
        print "WebSocket opened"

    def on_message(self, message):
        print message
        msg = json.loads(message)
        self.dispatcher.request_socket.send_json(msg)
        #self.write_message(u"You said: " + message)

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
    def __init__(self, loop):
        # Initialize ZMQ sockets
        ctx = zmq.Context()
        self.request_socket = ctx.socket(zmq.XREQ)
        self.request_socket.connect('tcp://%s:%d' % (KERNEL_IP, XREQ_PORT))
        self.sub_socket = ctx.socket(zmq.SUB)
        self.sub_socket.connect('tcp://%s:%d' % (KERNEL_IP, SUB_PORT))
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, '')
        
        self._make_streams(loop)
    
    def _make_streams(self, loop):
        self.sub_stream = zmqstream.ZMQStream(self.sub_socket, loop)
        self.req_stream = zmqstream.ZMQStream(self.request_socket, loop)

def main():
    # Tornado
    loop = ZMQLoop.instance()
    zmq_dispatcher = ZMQDispatcher(loop)
    handlers = [(r'/test', EchoWebSocket, dict(dispatcher=zmq_dispatcher)),]
    application = ZMQApplication(handlers)
    
    http_server = tornado.httpserver.HTTPServer(application, io_loop=loop)
    http_server.listen(9996)
    loop.start()

if __name__ == '__main__':
    main()
