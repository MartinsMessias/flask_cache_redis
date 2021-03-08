from flask import Flask
from flask_caching import Cache
from redis import Redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

cache = Redis(host='172.17.0.1', port=6379,
              password='', decode_responses=True)
