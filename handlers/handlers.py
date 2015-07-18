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

class HomeHandler(BaseHandler):
    def get(self):
        messages = self.application.syncdb.messages.find()
        self.render("slidy.html", messages=messages, notification=self.get_flash())