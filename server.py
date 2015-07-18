import tornado.httpserver
import tornado.ioloop
import tornado.options
import pymongo
import collections
import tornado.web
from operator import itemgetter
from tornado.options import define, options
import webbrowser
import Settings
import tornado.escape
from decorator import protected
from tornado.web import url
define("port", default=8888, help="run on the given port", type=int)

from handlers.handlers import * 

class Application(tornado.web.Application):
    def __init__(self, **overrides):
        handlers = [
            url(r'/auth/login/',AuthLoginHandler),
            url(r'/auth/logout/', AuthLogoutHandler),
            url(r'/register/', RegisterHandler),
	    url(r'/home/', HomePageHandler, name='home')
	]
	
        settings = {
            "template_path":Settings.TEMPLATE_PATH,
            "static_path":Settings.STATIC_PATH,
            "debug":Settings.DEBUG,
            "cookie_secret": Settings.COOKIE_SECRET,
            'xsrf_cookies': False,
            "login_url": "/auth/login/"
        }
        conn = pymongo.MongoClient("localhost", 27017)
        self.db = conn["jjaguar_database"]
        coll = self.db['auth_users']        
        tornado.web.Application.__init__(self, handlers, **settings)
                
if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()