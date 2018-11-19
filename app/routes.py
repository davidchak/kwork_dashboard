# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, jsonify
from models import User, Data, LoginForm
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    message = ''
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            message = u'Проверите правильность ввода логина или пароля!'
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('login.html', form = form, message = message)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    data = User.query.all()
    return render_template('dashboard.html', data = data)


@app.route('/api/get', methods=['GET','POST'])
def get_data():
    return jsonify({'status': 'success'})


@app.route('/api/set', methods=['POST'])
def set_data():
    data = request.get_json()
    # new_query = Data(id=data.id, datestamp=data.datestamp, json=date.json)
    # db.session.add(new_query)
    # db.session.commit()
    return jsonify({'status': 'success', 'data': data})

