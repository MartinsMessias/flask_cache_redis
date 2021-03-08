import os
import redis
from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

#Remote
cache = redis.from_url(os.environ.get("REDISTOGO_URL"))

#Localhost
#cache = redis.Redis(host='172.17.0.1', port=6379, password='')