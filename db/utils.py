from flask import app
from flask_mongoengine import MongoEngine
from mongoengine import connect


def connect_db():
    connect(host="mongodb://127.0.0.1:27017/Fundoo-notes")
