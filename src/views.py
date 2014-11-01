#! /usr/bin/env python2.7
# -*- coding: UTF-8 -*-

from flask import request, redirect
from src import app, db, models, lm
from flask.ext.login import login_user, logout_user, current_user, login_required

@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@app.route('/')
def index():
    article_list = models.Article.query.order_by(models.Article.create_time.desc()).all()
    s = '<ul>'
    for article in article_list:
        s += '<li><a href="/article/'+str(article.id)+'">'+article.name+'</a></li>'
    s += '</ul>'
    return s

@app.route('/article/<int:article_id>')
def article(article_id):
    article = models.Article.query.filter_by(id=article_id).one()
    return article.article

@app.route('/raw_article/<int:article_id>')
def get_rst(article_id):
    article = models.Article.query.filter_by(id=article_id).one()
    return article.rst

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
