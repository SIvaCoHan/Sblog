#! /usr/bin/env python2.7
# -*- coding: UTF-8 -*-

from datetime import datetime
from docutils.core import publish_parts
from flask.ext.sqlalchemy import SQLAlchemy
from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    passwd = db.Column(db.String(120), unique=True)

    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd 

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    article = db.Column(db.Text(), unique=True)
    rst = db.Column(db.Text(), unique=True)
    create_time = db.Column(db.DateTime())

    def __init__(self, rst, create_time=None):
        self.rst = rst
        _article = publish_parts(rst, writer_name="html")
        self.name = _article['title']
        self.article = _article['whole']
        if create_time is None:
            self.create_time = datetime.utcnow()
