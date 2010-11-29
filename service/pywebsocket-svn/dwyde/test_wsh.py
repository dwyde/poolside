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

def web_socket_transfer_data(request):    
    ctx = zmq.Context()
    loop = ioloop.IOLoop.instance()
    
    request_socket = ctx.socket(zmq.XREQ)
    request_socket.connect('tcp://%s:%d' % (KERNEL_IP, XREQ_PORT))
    
    class Responder(Thread):
        def __init__(self, line):
            Thread.__init__(self)
            self._line = line
        
        def run(self):
            loop.stop()
            msg = json.loads(self._line)
            request_socket.send_json(msg)
            recv_data()
            loop.start()
        
    def echo_client(arg_list):
        request.ws_stream.send_message(str(arg_list[0]))

    def send_data(line):
        resp = Responder(line)
        resp.start()
        
    def recv_data():
        line = request.ws_stream.receive_message()
        send_data(line)
    
    def listener():    
        s = ctx.socket(zmq.SUB)
        s.connect('tcp://%s:%d' % (KERNEL_IP, SUB_PORT))
        s.setsockopt(zmq.SUBSCRIBE, '')
        stream = zmqstream.ZMQStream(s, loop)
        stream.on_recv(echo_client)
        req_stream = zmqstream.ZMQStream(request_socket, loop)
        req_stream.on_recv(echo_client)
        print 'listening!'
    
    # Main loop
    listener()
    recv_data()
    while True:
        loop.start()


# vi:sts=4 sw=4 et
