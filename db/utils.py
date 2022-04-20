from flask import app
from flask_mongoengine import MongoEngine
from mongoengine import connect


def connect_db():
    connect(host="mongodb://127.0.0.1:27017/user-registration")
    # app.config['MONGODB_SETTINGS'] = {
    # 'db': '',
    # a'host': 'localhost',
    # 'port': 27017
    # }
    # db = MongoEngine()
    # db.init_app(app)
