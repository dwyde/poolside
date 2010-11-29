import json
import zmq
from zmq.eventloop import zmqstream, ioloop, stack_context
from threading import Thread

# ZMQ socket address constants
KERNEL_IP = '127.0.0.1'
XREQ_PORT = 5575
SUB_PORT = 5576

def web_socket_do_extra_handshake(request):
    pass  # Always accept.

class Responder(Thread):
    def __init__(self, controller, line):
        Thread.__init__(self)
        self._controller = controller
        self._line = line
    
    def run(self):
        self._controller.loop.stop()
        msg = json.loads(self._line)
        self._controller.request_socket.send_json(msg)
        self._controller.recv_data()
        self._controller.loop.start()

class RequestProcess:
    def __init__(self, request):
        self.request = request
        self.loop = ioloop.IOLoop.instance()
        self._zmq_sockets()
        self._make_listeners()

    def main_loop(self):
        self.recv_data()
        while True:
            self.loop.start()
            
    def _make_listeners(self):
        sub_stream = zmqstream.ZMQStream(self.sub_socket, self.loop)
        sub_stream.on_recv(self.echo_client)
        req_stream = zmqstream.ZMQStream(self.request_socket, self.loop)
        req_stream.on_recv(self.echo_client)
    
    def _zmq_sockets(self):
        ctx = zmq.Context()
        self.request_socket = ctx.socket(zmq.XREQ)
        self.request_socket.connect('tcp://%s:%d' % (KERNEL_IP, XREQ_PORT))
        
        self.sub_socket = ctx.socket(zmq.SUB)
        self.sub_socket.connect('tcp://%s:%d' % (KERNEL_IP, SUB_PORT))
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, '')
        
    def recv_data(self):
        line = self.request.ws_stream.receive_message()
        self.send_data(line)
        
    def echo_client(self, arg_list):
        self.request.ws_stream.send_message(str(arg_list[0]))

    def send_data(self, line):
        resp = Responder(self, line)
        resp.start()
        
def web_socket_transfer_data(request):    
    process = RequestProcess(request)
    process.main_loop()
    

# vi:sts=4 sw=4 et
