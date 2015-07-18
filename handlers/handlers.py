import base64
from bson.objectid import ObjectId
import os
import urllib
import tornado.auth
import tornado.escape
import tornado.gen
import tornado.httpserver
import logging
import bson.json_util
import json
import urlparse
import time
import threading
from tornado.ioloop import IOLoop
from tornado.web import asynchronous, RequestHandler, Application
from tornado.httpclient import AsyncHTTPClient


class BaseHandler(RequestHandler):
    def get_login_url(self):
        return u"/auth/login/"

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None
        
# Purpose: Login page checks for permission                
class AuthLoginHandler(BaseHandler):
    def get(self):
        self.render ("login.html")

    def post(self):  
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        user = self.application.db['auth_users'].find_one({username: password})

        if user:
            self.set_current_user(username)
            self.redirect('/home/')
        else:
            self.redirect(u'/auth/login/')
        

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
    @tornado.web.authenticated
    def get(self):   
        self.render("home.html")
class RegisterHandler(AuthLoginHandler):
    def get(self):
        self.render("register.html")
    
    def post(self):
        username = self.get_argument("username", "")
        names = list(self.application.db['auth_users'].find())
        for each in names:
            print each
            try:
                if each[username]:
                    error_msg = u"?error=" + tornado.escape.url_escape("Login name already taken")
                    self.redirect(u"/login" + error_msg)   
            except KeyError: 
                pass
        password = self.get_argument('password', '')
        user = {}
        user[username] = password
        self.application.db['auth_users'].insert_one(user)
        print list(self.application.db['auth_users'].find())
        self.set_current_user(username)
        self.redirect('/home/')
        

        