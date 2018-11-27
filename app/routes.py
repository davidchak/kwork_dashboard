# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, jsonify, abort, Response
from models import User, Data, Parser, LoginForm, AddUserForm, NewParserForm, Client
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash
from app import app, db
from flask_security import login_required, current_user
from flask_principal import RoleNeed, Permission


admin_permission = Permission(RoleNeed('admin'))


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


# Выход
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


# Додашборд
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


# Панель добавления пользователей
@app.route('/users', methods=['GET', 'POST'])
def get_users():
    
    if admin_permission.can():
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

    return redirect(url_for('dashboard'))
        

# Удаление пользователя
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


# Удаление парсера
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


# Добавление нового клиента
@app.route('/add_client', methods=['POST'])
@login_required
def add_client():

    new_client = Client()
    new_client.name = request.form['client_name']
    new_client.generate_key()
    new_client.generate_sicret()
    count = request.form['days']
    new_client.extend_life_marker(count)
    
    try:
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'status': 'success'})
    
    except:
        return jsonify({'status': 'error'})


# API
@app.route('/api/v1.0/get', methods=['GET','POST'])
def get_data():
    
    return jsonify({'status': 'success'})


@app.route('/api/v1.0/get_last/<count>', methods=['GET'])
def get_last(count):
    
    data_list = []
    data = db.session.query(Data).order_by(Data.id.desc()).limit(count)

    for item in data:
        new_item = {
            'id': item.id,
            'parser_id': item.parser_id,
            'datestamp': item.datestamp,
            'json': item.json
        }
        data_list.append(new_item)

    return jsonify({'result': data_list})


@app.route('/api/v1.0/set', methods=['POST'])
def set_data():
    
    data = request.json
    result = Parser.query.filter_by(name = data['ID']).first()
    
    if not result:
        return jsonify({'status': 'not found parser name'})
    
    d = Data()
    d.datestamp = data['datestamp']
    d.parser_id = data['ID']
    d.json = str(data['json'])
    db.session.add(d)
    db.session.commit() 
    
    return jsonify({'result': data})

# TODO: Зарегистрировать ошибку! 
# сейчас не работает
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404