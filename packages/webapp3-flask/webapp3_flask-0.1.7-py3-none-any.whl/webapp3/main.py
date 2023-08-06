from flask import Flask, session,request,redirect, url_for
import io
import os


app = Flask(__name__)


def webapp(arg):
    if request.method == 'GET':    
        return webappGet(arg)
    if request.method == 'POST':
        return webappPost(arg)

class Response:
  def __init__(self, handler):
    self.handler = handler

  def write(self, stuffAdd):
    self.handler.data += stuffAdd

class ReqFile:
  def get(self,arg):
    file = request.files[arg]
    return file

class DaRequest:
  def __init__(self):
    self.remote_addr = request.remote_addr
    self.POST = ReqFile()

  def get(self,arg):
    return request.form.get(arg)

  

class BaseHandler:
  
  def __init__(self):
    self.data = ""
    self.ChangePage="None"
    self.response = Response(self)
    self.session = session
    self.request= DaRequest()
  def redirect(self,arg):
    self.ChangePage=arg

class RequestHandler(BaseHandler):
  pass

class webapp2:
  RequestHandler = RequestHandler

def webappGet(daPage):
    daPage.get()
    if daPage.ChangePage=="None":
        return daPage.data
    else:
        return redirect(daPage.ChangePage)

def webappPost(daPage):
    daPage.post()
    if daPage.ChangePage=="None":
        return daPage.data
    else:
        return redirect(daPage.ChangePage)
    



