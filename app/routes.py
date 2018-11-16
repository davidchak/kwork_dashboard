# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from .models import User, LoginForm
from flask_login import login_user, login_required, logout_user
from . import app
from . import db


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name= form.name.data).first()
        print(user.name)
        if user is not None and user.check_password(form.passwd.data):
            login_user(user)
            return redirect('/dashboard')
    return render_template('login.html', form = form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashbord():
    data = User.query.all()
    return render_template('dashbord.html', data = data)


