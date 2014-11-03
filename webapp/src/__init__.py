#! /usr/bin/env python2.7
# -*- coding: UTF-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'guess'
db = SQLAlchemy(app)
lm = LoginManager()
lm.login_view='/'
lm.init_app(app)

from src import views, models
