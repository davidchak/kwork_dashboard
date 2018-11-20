# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, jsonify
from models import User, Data, Parser, LoginForm, AddUserForm, NewParserForm
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
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
    return render_template('login.html', form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    form = NewParserForm()
    data = Parser.query.all()

    if form.validate_on_submit():
        name = form.name.data.lower()
        parser = Parser(name=name)
        db.session.add(parser)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', data = data, form = form)


@app.route('/users', methods=['GET', 'POST'])
@login_required
def get_users():

    form = AddUserForm()
    data = User.query.all()

    if form.validate_on_submit():
        name = form.name.data.lower()
        passwd = form.password.data

        if name and passwd:
            user = User.query.filter_by(name=name).first()
            if not user:
                user = User(name=name)
                user.password_hash = generate_password_hash(passwd)
                db.session.add(user)
                db.session.commit()
            return redirect(url_for('get_users'))

    return render_template('users.html', data = data, form=form)


@app.route('/del_user', methods=['POST'])
@login_required
def del_user():
    
    user_id = request.form['id']
    user = User.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'})


@app.route('/del_parser', methods=['POST'])
@login_required
def del_parser():

    parser_id = request.form['id']
    parser = Parser.query.filter_by(id=parser_id).first()
    if parser:
        db.session.delete(parser)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'})


# API
@app.route('/api/get', methods=['GET','POST'])
def get_data():
    return jsonify({'status': 'success'})


@app.route('/api/set', methods=['POST'])
def set_data():
    data = request.json['data']
    if not data:
        return jsonify({'status': 'error'})
    return jsonify({'result': data})



    

