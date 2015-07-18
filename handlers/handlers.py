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
        return u"/login"

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None
        
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
        
        auth = self.check_permission(password, username)
        if auth:
            self.set_current_user(username)
            self.redirect('/home/')
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
    def get(self):   
        self.render("home.html")
