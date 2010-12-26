import tornado.httpserver
import tornado.ioloop
import tornado.auth
import tornado.websocket

import json
import zmq
from zmq.eventloop import zmqstream

# ZMQ socket address constants
KERNEL_IP = '127.0.0.1'
XREQ_PORT = 5575
SUB_PORT = 5576
ALT_XREQ = 5578
ALT_SUB = 5579

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, ports=(0, 0)):
        tornado.websocket.WebSocketHandler.__init__(self, application, request)
        self._make_msg_dict()
        self.dispatcher = ZMQDispatcher(ports)
    
    def open(self):
        if not self.get_current_user():
            self.close()
        
        self.dispatcher.sub_stream.on_recv(self.write_wrapper)
        self.dispatcher.req_stream.on_recv(self.write_wrapper)

    def on_message(self, message):
        msg = json.loads(message)
        self.dispatcher.request_socket.send_json(msg)

    def on_close(self):
        print "WebSocket closed"
        
    def _make_msg_dict(self):
        self.msg_dict = {}
        # IPython
        self.msg_dict.update({
            'pyin': lambda x: {'input': x['code']},
            'pyout': lambda x: {'output': x['data']},
            'pyerr': lambda x: {'output': x['ename'] + '<br />' + x['evalue']},
        })
        
    def write_wrapper(self, message_parts):
        for part in message_parts:
            msg = json.loads(part)
            msg_type = msg.get('msg_type')
            if msg_type in self.msg_dict:
                result = self.msg_dict[msg_type](msg['content'])
                result.update({'target': msg['parent_header']['msg_id']})
                print result
                self.write_message(result)
        
    def close(self):
        print 'closing'
        self.stream.close()
        
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)
        

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
