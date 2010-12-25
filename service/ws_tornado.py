import tornado.httpserver
import tornado.ioloop
from tornado import websocket

class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"

    def on_message(self, message):
        print message
        self.write_message(u"You said: " + message)

    def on_close(self):
        print "WebSocket closed"


application = tornado.web.Application([
        (r"/test", EchoWebSocket),
        ], static_path=".")
   
http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(9996)
tornado.ioloop.IOLoop.instance().start()
