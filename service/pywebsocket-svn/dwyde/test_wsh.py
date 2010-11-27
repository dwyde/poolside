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


_GOODBYE_MESSAGE = 'Goodbye'
KERNEL_IP = '127.0.0.1'
KERNEL_PORT = 5575

def web_socket_do_extra_handshake(request):
    pass  # Always accept.


def web_socket_transfer_data(request):    
    connection = ('tcp://%s' % KERNEL_IP) + ':%i'
    req_conn = connection % KERNEL_PORT
    sub_conn = connection % (KERNEL_PORT + 1)

    # Create sockets
    c = zmq.Context()
    request_socket = c.socket(zmq.XREQ)
    request_socket.connect(req_conn)
    sub_socket = c.socket(zmq.SUB)
    sub_socket.connect(sub_conn)
    sub_socket.setsockopt(zmq.SUBSCRIBE, '')
    
    p = zmq.Poller()
    p.register(sub_socket)
    
    while True:
        line = request.ws_stream.receive_message()
        msg = json.loads(line)['json']
        # Send data
        request_socket.send_json(msg)

        # Receive a response

        while True:
            res = p.poll(500)
            if res == []:
                break
            else:
                result = sub_socket.recv(zmq.NOBLOCK)
                print result
                request.ws_stream.send_message(result)
            #result = sub_socket.recv_json()
        
        if line == _GOODBYE_MESSAGE:
            return


# vi:sts=4 sw=4 et
