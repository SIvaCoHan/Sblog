#! /usr/bin/env python2.7
# -*- coding: UTF-8 -*-

from time import time
from flask import request, redirect
from flask import Response
from src import app, db, models, lm
from flask.ext.login import login_user, logout_user, current_user, login_required

class FOOL_CACHE():
    '''
    Don't do this like me.
    it is fool
    '''
    def __init__(self):
        self.cache = {}
        pass

    def get(self, key):
        try:
            ret = self.cache[key]
        except KeyError:
            return None
        if time() - ret['utc'] > 60:
            del self.cache[key]
            return None
        return ret['value']

    def set(self, key, value):
        self.cache[key] = {'value':value, 'utc':time()}

CACHE = FOOL_CACHE()

@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@app.route('/')
def index():
    article_list = models.Article.query.order_by(models.Article.create_time.desc()).all()
    ret = CACHE.get('index.s')
    if ret:
        return ret
    s = '<ul>'
    for article in article_list:
        s += '<li><a href="/article/'+str(article.id)+'">'+article.name+'</a></li>'
    s += '</ul>'
    CACHE.set('index.s', s)
    return s

@app.route('/article/<int:article_id>')
def article(article_id):
    ret = CACHE.get('article.s')
    if ret:
        return ret
    article = models.Article.query.filter_by(id=article_id).one()
    CACHE.set('article.s', article.article)
    return article.article

@app.route('/raw_article/<int:article_id>')
def get_rst(article_id):
    ret = CACHE.get('article.rst')
    if ret:
        return Response(ret, mimetype='text/plain')
    article = models.Article.query.filter_by(id=article_id).one()
    CACHE.set('article.rst', article.rst)
    return Response(article.rst, mimetype='text/plain')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return '<form action="#" method="post"><input type="text" name="username" placeholder="username"><input type="password" name="passwd" placeholder="password"><input type="submit"/></form>'
    if request.method == 'POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')
        u = models.User.query.filter_by(username=username).filter_by(passwd=passwd).first()
        if u is None:
            return redirect('/')
        login_user(u)
        return redirect('/new')

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/new', methods=['POST', 'GET'])
@login_required
def new_article():
    if request.method == 'GET':
        return '<form action="#" method="post"><textarea name="p"></textarea><input type="submit"/></form>'
    if request.method == 'POST':
        p = request.form.get('p')
        article = models.Article(p)
        db.session.add(article)
        db.session.commit()
        return redirect('/')
