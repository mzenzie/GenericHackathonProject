import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from operator import itemgetter
from tornado.options import define, options
import webbrowser
import Settings
import tornado.escape
from decorator import protected
define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainPageHandler),
            (r"/auth/login/",AuthLoginHandler),
            (r"/home/", HomePageHandler),
            (r"/auth/logout/", AuthLogoutHandler),
	    
	    url(r'/', HomeHandler, name='home')
	]
	
        settings = {
            "template_path":Settings.TEMPLATE_PATH,
            "static_path":Settings.STATIC_PATH,
            "debug":Settings.DEBUG,
            "cookie_secret": Settings.COOKIE_SECRET,
            "login_url": "/auth/login/"
        }
        tornado.web.Application.__init__(self, handlers, **settings)
        

# Purpose: Getting the current user
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

# Purpose: Redirects to the home page
class MainPageHandler(BaseHandler):
    @protected
    def get(self):
        self.redirect('/auth/login/')
        
# Purpose: Login page checks for permission                
class AuthLoginHandler(BaseHandler):
    def get(self):

        errormessage = ""
        try:
            errormesage = self.get_argument("error")
        except:
            errormessage = ""
        self.render ("login.html", errormessage = errormessage)
        
    def check_permission(self, password, username):
        usernames = ["azheng", "dzelin", "mzenzie"]
        if username in usernames and password == "Welcome1":
            return True
        return False

    def post(self):  
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        #helper.set_username(username)
        
        auth = self.check_permission(password, username)
        if auth:
            self.set_current_user(username)
            self.redirect('/home/')
            #self.redirect(self.get_argument("next", u"/home/"))
        else:
            form = """<form method = "post" class = "container">
            <p> <form action = "localhost:8888/login/"></form></p>
            <h3>Incorrect Username or Password. </h3>
            <p>
            
            <form action = "http://localhost:8888/">
            <input type = "submit" value = "Try again">
            </form>
            
            </p>
            </form>"""
            self.write(form)
        

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")
            
# Logout page clears cookie        
class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))
        
class HomePageHandler(BaseHandler):
    @protected
    def get(self):   
        self.write("Welcome to the home page")
	render_sidebar(self)


                
if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()