import json
import zmq
from zmq.eventloop import zmqstream, ioloop, stack_context
from threading import Thread

from rpc_methods import Methods

# ZMQ socket address constants
KERNEL_IP = '127.0.0.1'
XREQ_PORT = 5575
SUB_PORT = 5576

def web_socket_do_extra_handshake(request):
    '''
    Possibly run an extra security "handshake" test.
    For now, we assume that the initial check is sufficient.
    '''
    pass

class RequestProcess:
    '''
    Class for handling a websocket stream.
    Each response from IPython is sent back to the websocket, via a new thread.
    '''
    
    def __init__(self, request):
        self.request = request
        self.loop = ioloop.IOLoop.instance()
        self._zmq_sockets()
        self._make_listeners()
        
    def _zmq_sockets(self):
        '''Open XREQ and SUB sockets for interacting with an IPython kernel.'''
        ctx = zmq.Context()
        self.request_socket = ctx.socket(zmq.XREQ)
        self.request_socket.connect('tcp://%s:%d' % (KERNEL_IP, XREQ_PORT))
        
        self.sub_socket = ctx.socket(zmq.SUB)
        self.sub_socket.connect('tcp://%s:%d' % (KERNEL_IP, SUB_PORT))
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, '')
            
    def _make_listeners(self):
        '''Associate a callback function with the opened ZMQ sockets.'''
        sub_stream = zmqstream.ZMQStream(self.sub_socket, self.loop)
        sub_stream.on_recv(self.echo_client)
        req_stream = zmqstream.ZMQStream(self.request_socket, self.loop)
        req_stream.on_recv(self.echo_client)

    def _raw_ws_socket(self, raw_socket):
        pass
        #self.loop.add_handler(raw_socket.fileno(), self.echo_client, self.loop.READ)
        #self.loop.add_handler(raw_socket.fileno(), self.echo_client, self.loop.WRITE)

    def main_loop(self):
        '''Wait to receive data from the websocket.'''
        #self.loop.start()
        while True:
            self.recv_data()
            #self.loop.start()
        
    def recv_data(self):
        '''Receive a message from the websocket and send it forward.'''
        #self.loop.stop()
        line = self.request.ws_stream.receive_message()
        if self.loop.running():
            self.loop.stop()
        self.handle(line)
        self.loop.start()
        
    def echo_client(self, arg_list):
        '''Callback: send data back to the websocket.'''
        self.loop.stop()
        msg = json.loads(arg_list[0])
        print msg['msg_type']
        #print arg_list
        self.request.ws_stream.send_message(str(arg_list[0]))
        self.loop.start()
        
    def handle(self, line):
        msg = json.loads(line)
        self.request_socket.send_json(msg)


def web_socket_transfer_data(request):
    '''Receive, and respond to, websocket input (in a loop).'''
    raw_socket = request.connection._request_handler.server.socket
    process = RequestProcess(request)
    process._raw_ws_socket(raw_socket)
    process.main_loop()
    
