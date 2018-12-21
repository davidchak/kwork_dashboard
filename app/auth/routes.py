# -*- coding: utf-8 -*-

from flask import redirect, render_template, url_for
from flask_login import login_user, logout_user
from flask_security import current_user
from app.models import User, LoginForm
from . import auth
from datetime import datetime


@auth.route('/login', methods=['GET', 'POST'])
def login():  
    
    form = LoginForm()
 
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data.lower()).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
    
            return redirect(url_for('auth.login'))
    
        login_user(user)
        user._update_last_login_time(datetime.now())
 
        return redirect(url_for('dashboard.get_user_page', id=user.id))
    
    return render_template('login.html', form = form)


@auth.route("/logout")
def logout():

    user = User.query.filter_by(name = current_user.name).first()
    user._update_last_logout_time(datetime.now())
    logout_user()
    return redirect(url_for('auth.login'))