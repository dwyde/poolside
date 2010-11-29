# Copyright 2009, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json
import zmq
from zmq.eventloop import zmqstream, ioloop, stack_context
from threading import Thread

_GOODBYE_MESSAGE = 'Goodbye'
KERNEL_IP = '127.0.0.1'
KERNEL_PORT = 5575

def web_socket_do_extra_handshake(request):
    pass  # Always accept.


def web_socket_transfer_data(request):    
    ctx = zmq.Context()
    loop = ioloop.IOLoop.instance()
    
    request_socket = ctx.socket(zmq.XREQ)
    request_socket.connect('tcp://127.0.0.1:5575')
    
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
        s.connect('tcp://127.0.0.1:5576')
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
