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
import pymongo


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
	d = doc['old_recs']
	from collections import OrderedDict
	from operator import itemgetter
	d = OrderedDict(sorted(d.items(), key=itemgetter(1)))	
	self.render('home.html', user= self.get_current_user(), doc = doc, d= d)

class AccountPageHandler(BaseHandler):
    def get(self):
	conn = pymongo.MongoClient()
	db = conn['jjaguar_database']
	coll = db['account_info']
	user = self.get_current_user()
	
	print 'user:', user
	
        languages = ['python', 'java', 'javascript', 'c', 'clojure', 'c#']
	
	user_doc = coll.find_one({'name': user})
	if user_doc:
	    old_recs = user_doc.get('old_rec')
	    exceptions = user_doc.get('exceptions')
	    skills = user_doc.get('exceptions')
	else:
	    user_doc = {
	        'name': user,
	        'exceptions': [],
	        'old_rec': {}
	    }
	    old_recs = {}
	    exceptions = []

	recs = []
	count = 0
	for w in sorted(old_recs, key=old_recs.get, reverse=True):
	    recs.append([w, old_recs[w]])
	    
	self.render('account.html', languages = languages, exceptions = exceptions, old_recs = recs, user = user, new = False)

    def post(self):
	
	exceptions = []
	recs = []	
	languages = ['python', 'java', 'javascript', 'c', 'clojure', 'c#']
	old_recs = {'python': 0.40, 'java': 0.90, 'c#': 0.10}
	count = 0
	for w in sorted(old_recs, key=old_recs.get, reverse=True):
	    recs.append([w, old_recs[w]])	

	input0 = self.get_argument('bad_lang0')
	if input0 not in exceptions:
	    exceptions.append(input0)	
	try:
	    input1 = self.get_argument('bad_lang1')
	    if input1 and input1 not in exceptions:
		exceptions.append(input1)	    
	    try:
		input2 = self.get_argument('bad_lang2')
		if input2 and input2 not in exceptions:
		    exceptions.append(input2)
	    except:
		print 'nope'
	except:
	    print 'nope'
		    
	self.render('account.html', languages = languages, exceptions = exceptions, old_recs = recs, user = 'Danielle', new = False)
	



class LearnPageHandler(BaseHandler):
    def get(self):
	self.render('learn.html')

    def post(self):
	
	
	self.redirect('/result/')
class ResultPageHandler(BaseHandler):
    def get(self):
	self.render('sidebar.html')
    def post(self):
	constraints = {}
	id_type = self.get_argument('type')
	process = self.get_argument('process')
	functional = self.get_argument('Functional')
	typing = self.get_argument('typing')
	self.write('You chose {}, {}, {}, {}'.format(id_type, process, functional, typing))
	if id_type == 'imperative':
	    constraints['imperative'] = 'y'
	else:
	    constraints['imperative'] = 'n'
	if process == 'compiled':
	    constraints['compiled'] = 'y'
	else:
	    constraints['compiled'] = 'n'
	if functional == 'functional':
	    constraints['functional'] = 'y'
	else:
	    constraints['functional'] = 'n'
	if typing == "dynamic":
	    constraints['typing'] = 'd'
	else:
	    constraints['typing'] = 's'
	self.write('\n')
	self.write(constraints)

	
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