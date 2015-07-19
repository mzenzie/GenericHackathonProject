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
	
class HomePageHandler(BaseHandler):
    def get(self):   
	doc = {"name": "azheng", "skill": {"python": 7, "c": 3}, "old_recs":{"c": 90, "python": 10}}
	#old_recs = {'python': 0.40, 'java': 0.90, 'c#': 0.10}
	d = doc['old_recs']
	print d
	from collections import OrderedDict
	from operator import itemgetter
	d = OrderedDict(sorted(d.items(), key=itemgetter(1)))	
	print d	
	print doc
	self.render('home.html', user= self.get_current_user(), doc = doc, d= d)

class AccountPageHandler(BaseHandler):
    def get(self):
        languages = ['python', 'java', 'javascript', 'c']
	old_recs = {'python': 0.40, 'java': 0.90, 'c#': 0.10}
	from collections import OrderedDict
	from operator import itemgetter
	d = OrderedDict(sorted(old_recs.items(), key=itemgetter(1)))	
	print d
	self.render('account.html', languages = languages, old_recs = old_recs, user = 'Danielle')

class LearnPageHandler(BaseHandler):
    def get(self):
	self.render('learn.html')
    #def post(self):
	#form = """
	#<script scr = "/static/js/jquery-1.7.2.min.js"></script>
	
	#var boxes = $('input[name = location]:checked');
	#var boxesValue = [];
	#$(boxes).each(function(){
	#boxesValue.push(value);
	#});
	#"""
	#self.write(form)
	
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