from flask import Flask
from flask_caching import Cache
import redis
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

cache = redis.from_url(os.environ.get("REDIS_URL"))
