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
        self.render('sidebar.html')

class AccountPageHandler(BaseHandler):
    def get(self):
        languages = ['python', 'java', 'javascript', 'c']	
	self.render('account.html', languages = languages)

class LearnPageHandler(BaseHandler):
    def get(self):
	self.write('learn page handler')
    

class DefPageHandler(BaseHandler):
    def get(self):
	form = """<h3>Here are a few terms to understand before we recommend a dictionary:</h3>
		<p>Imperative - focuses on describing how a program operates, defines sequences of commands for the computer to perform</p>
		<p>Declarative - describes what the program should accomplish, rather than describing how to go about accomplishing it as a sequence of the commands </p>
		<p>Static Typing - the type of a variable is known at compile time, the user must declare the type of each variable</p>
		<p>Dynamic Typing - allows you to provide type information, but do not require it</p>
		<p>Compiled language - </p>
		<p>Interpreted language- most of its implementations execute instructions directly, without previously compiling a program into machine-language instructions</p>
		<p>Functional - functions, not objects or procedures, are used as the fundamental building blocks of a program</p></h3>"""
	self.write(form)