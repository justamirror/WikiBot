from threading import Thread
from flask import Flask
import os
app = Flask(__name__)
@app.route('/')
def home():
    return "E"
def run():
   app.run(host='0.0.0.0',port=8080)
def start():
    t = Thread(target=run)
    t.start()