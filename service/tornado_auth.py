import tornado.httpserver
import tornado.ioloop
import tornado.auth
import tornado.web

BASE_URL = 'http://localhost:5984/notebook/_design/notebook/_rewrite/all'

class AuthApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/login', AuthLoginHandler),
            (r'/logout', AuthLogoutHandler),
        ]
        settings = dict(
            cookie_secret="secret_ha$h",
            login_url="/auth/login",
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)

class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect(ax_attrs=["name"])

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        self.set_secure_cookie("user", tornado.escape.json_encode(user), expires_days=0.1)
        self.redirect(BASE_URL) # broken link, for now

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.write("You are now logged out")

def main():
    application = AuthApplication()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9997)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
