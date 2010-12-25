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

ctx = zmq.Context()

request_socket = ctx.socket(zmq.XREQ)
request_socket.connect('tcp://%s:%d' % (KERNEL_IP, XREQ_PORT))
sub_socket = ctx.socket(zmq.SUB)
sub_socket.connect('tcp://%s:%d' % (KERNEL_IP, SUB_PORT))
sub_socket.setsockopt(zmq.SUBSCRIBE, '')

class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"

    def on_message(self, message):
        msg = json.loads(message)
        request_socket.send_json(msg)
        #self.write_message(u"You said: " + message)

    def on_close(self):
        print "WebSocket closed"


class ZMQApplication(tornado.web.Application):
    
    def __init__(self, zmq_stream, handlers, *args, **kwargs):
        tornado.web.Application.__init__(self, handlers, *args, **kwargs)
        self._zmq_stream = zmq_stream
        self._zmq_stream.on_recv(self._handle_zmq_msg)
    
    def _handle_zmq_msg(self, msg):
        print '?', msg
        
    def echo_client(self, *args):
        print args

class ZMQLoop(tornado.ioloop.IOLoop):
    NONE = 0
    READ = zmq.POLLIN
    WRITE = zmq.POLLOUT
    ERROR = zmq.POLLERR
    
    def __init__(self, impl=None):
        tornado.ioloop.IOLoop.__init__(self, impl=zmq.Poller())

def main():
    loop = ZMQLoop.instance()
    
    stream = zmqstream.ZMQStream(sub_socket, loop)
    
    handlers = [(r'/test', EchoWebSocket),]
    application = ZMQApplication(stream, handlers)
       
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9996)
    
    #loop = ioloop.IOLoop.instance()
    #sl = SetupLoop(loop)
    loop.start()

if __name__ == '__main__':
    main()
