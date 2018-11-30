# -*- coding: utf-8 -*-

from flask import redirect, render_template, url_for
from flask_login import login_user, logout_user
from flask_security import current_user
from app.models import User, LoginForm
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():  
    
    form = LoginForm()
 
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data.lower()).first()
    
        if user is None or not user.check_password(form.password.data):
            message = u'Проверите правильность ввода логина или пароля!'
    
            return redirect(url_for('auth.login'))
    
        login_user(user)
 
        if current_user.has_role('admin'):
            return redirect(url_for('dashboard.get_admin_page', username=user.name))
        elif current_user.has_role('moderator'):
            return redirect(url_for('dashboard.get_moderator_page', username=user.name))
    
    return render_template('login.html', form = form)


# Выход
@auth.route("/logout")
def logout():
    
    logout_user()
    return redirect(url_for('auth.login'))