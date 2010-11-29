import json
import zmq
from zmq.eventloop import zmqstream, ioloop, stack_context
from threading import Thread

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

class Responder(Thread):
    '''
    Create a new thread for responding via a websocket.
    Mostly just calls methods of RequestProcess.
    '''
    
    def __init__(self, controller, line):
        '''
        Class constructor.
        :param controller: an instance of the RequestProcess class
        :param line: a string to be sent through the websocket
        '''
        
        Thread.__init__(self)
        self._controller = controller
        self._line = line
    
    def run(self):
        '''Pause the ZMQ event loop, then resume it when we're done.'''
        
        self._controller.loop.stop()
        msg = json.loads(self._line)
        self._controller.request_socket.send_json(msg)
        self._controller.recv_data()
        self._controller.loop.start()

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

    def main_loop(self):
        '''Wait to receive data from the websocket.'''
        self.recv_data()
        while True:
            self.loop.start()
            
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
        
    def recv_data(self):
        '''Receive a message from the websocket and send it forward.'''
        line = self.request.ws_stream.receive_message()
        self.send_data(line)
        
    def send_data(self, line):
        '''Use a new thread to respond to websocket input.'''
        resp = Responder(self, line)
        resp.start()
        
    def echo_client(self, arg_list):
        '''Callback: send data back to the websocket.'''
        self.request.ws_stream.send_message(str(arg_list[0]))


def web_socket_transfer_data(request):
    '''Receive, and respond to, websocket input (in a loop).'''
    process = RequestProcess(request)
    process.main_loop()
    
