# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect
from . import dashboard
from flask import jsonify, request, current_app
from flask_security import login_required, roles_required, roles_accepted, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Data, User, Parser, Client, Role


# Главная пустая
@dashboard.route('/', methods=['GET'])
@login_required
def get_index_page():

    if current_user.is_authenticated and current_user.has_role('admin'):
        return redirect(url_for('dashboard.get_admin_page', username=current_user.name))
    elif current_user.is_authenticated and current_user.has_role('moderator'):
        return redirect(url_for('dashboard.get_moderator_page', username=current_user.name))
    else:
        return redirect(url_for('auth.login'))


# Админка
@dashboard.route('/admin_panel/<username>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def get_admin_page(username):
    
    users = User.query.all()
    parsers = Parser.query.all()
    clients = Client.query.all()
    clients_count = Client.query.count()
    parsers_count = Parser.query.count()
    
    admins_role = Role.query.filter_by(name='admin').first()
    admins_count = db.session.query(User).filter(User.roles.contains(admins_role)).count()
    moderators_role = Role.query.filter_by(name='moderator').first()
    moderators_count = db.session.query(User).filter(User.roles.contains(moderators_role)).count()

    return render_template('admin.html', clients=clients, users=users, parsers=parsers, clients_count=clients_count, parsers_count=parsers_count, moderators_count=moderators_count, admins_count=admins_count)


# Модераторка
@dashboard.route('/moderator_panel/<username>', methods=['GET', 'POST'])
@login_required
@roles_required('moderator')
def get_moderator_page(username):

    clients = Client.query.filter_by(user_id = current_user.id).all()

    return render_template('moderator.html', clients=clients)



############################################################################################################
#     API для личного кабинета
############################################################################################################
# Добавление пользователя                 /dash/v1.0/user/add_user                        - для авторизованного админа
# Удаление пользователя                   /dash/v1.0/user/del_user                        - для авторизованного админа
#
# Добавление парсера                      /dash/v1.0/parser/add_parser                    - для авторизованного админа
# Удаление парсера                        /dash/v1.0/parser/del_parser                    - для авторизованного админа
# Получение n-последних записеё парсера   /dash/v1.0/parser/get_last_query/<int>          - для авторизованного админа
#
# Добавление клиента                      /dash/v1.0/client/add_client                    - для авторизованного админа или модератора
# Удаление клиента                        /dash/v1.0/client/del_client                    - для авторизованного админа или модератора
#
# Получение количества зарег.             /dash/v1.0/dashboard/get_admin_info  - для авторизованного админа
# Получение количества зарег.             /dash/v1.0/dashboard/get_moderator_info  - для авторизованного админа
#
#
# Формат ответа сервера(api):
# api_resp = {
#     'url': '/api/v1.0/add_user',      - url запроса
#     'method': 'POST',                 - метод запроса
#     'success': True,                  - результат выполнения
#     'resp_data': 'data'               - ответ сервера(если нужены какие-либо данные)
#     'error': 'Error'                  - ошибки, если они были
# }


api_resp = {
    'url': '',     
    'method': '',                 
    'success': True,                 
    'resp_data': '',               
    'error': ''                
}


# Добавление пользователя 
@dashboard.route('/dash/v1.0/add_user', methods=['POST'])
@roles_required('admin')
def add_user():

    username = request.form['name']
    password = request.form['password']
    role = request.form['role']

    api_resp['url'] = '/dash/v1.0/add_user'
    api_resp['method'] = 'POST'
    
    unique_test = User.query.filter_by(name = username).first()

    if unique_test:
        api_resp['success'] = False
        api_resp['error'] = 'The user is already in the database'

    user = current_app.user_datastore.create_user(name=username)
    user.password_hash = generate_password_hash(password)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
        api_resp['success'] = False
        api_resp['error'] = 'Add user error'

        return jsonify(api_resp)

    role = Role.query.filter_by(name=role).first()
    
    if role:    
        current_app.user_datastore.add_role_to_user(user, role)
        
        try:
            db.session.commit()
        except:
            db.session.rollback()
            api_resp['success'] = False
            api_resp['error'] = 'Add role to user error'
        return jsonify(api_resp)
    
    api_resp['success'] = True
    
    return jsonify(api_resp)


# Удаление пользователя 
@dashboard.route('/dash/v1.0/del_user', methods=['POST'])
@roles_required('admin')
def del_user(username):

    api_resp['url'] = '/dash/v1.0/del_user'
    api_resp['method'] = 'POST'
    
    user = User.query.filter_by(name=username).first()
    if user and user.name != current_user.name:
        try:
            db.session.delete(user)
            db.session.commit()
            api_resp['success'] = True
        except:
            api_resp['success'] = False
            api_resp['error'] = 'Add user error'
    
    return jsonify(api_resp)


# Добавление парсера 
@dashboard.route('/dash/v1.0/add_parser', methods=['POST'])
@roles_required('admin')
def add_parser():
    pass


# Удаление парсера 
@dashboard.route('/dash/v1.0/del_parser', methods=['POST'])
@roles_required('admin')
def del_parser(pansername):
    pass


# Добавление клиента 
@dashboard.route('/dash/v1.0/client/add_client', methods=['POST'])
@roles_accepted('moderator')
def add_client():

    name = request.form['name']

    api_resp['url'] = '/dash/v1.0/client/add_user'
    api_resp['method'] = 'GET'
    
    new_client = Client(name=name)
    new_client.user = current_user
    new_client.get_token()
    
    try:
        db.session.add(new_client)
        db.session.commit()
        api_resp['success'] = True
        api_resp['data'] = {'token': new_client.token}
    except:
        api_resp['error'] = 'Add client error'
        return jsonify(api_resp)
    
    api_resp['success'] = True
    
    return jsonify(api_resp)


# Удаление клиента 
@dashboard.route('/dash/v1.0/del_client', methods=['POST'])
@roles_accepted('admin', 'moderator')
def del_client(name):
    pass


# Получение n-последних записей парсера
@dashboard.route('/dash/v1.0/parser/get_last_query/<int:count>', methods=['GET'])
@roles_required('admin')
def get_last_query(count):
    
    api_resp['url'] = '/dash/v1.0/add_user'
    api_resp['method'] = 'GET'

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

    api_resp['success'] = True
    api_resp['data'] = data_list

    return jsonify(api_resp)



# Информация для панели управления
# общая для модератора!
@dashboard.route('/dash/v1.0/dashboard/get_moderator_info', methods=['GET'])
@roles_required('moderator')
def get_moderator_info():

    api_resp['url'] = '/dash/v1.0/dashboard/get_moderator_info'
    api_resp['method'] = 'GET'

    try:
        clients_count = current_user.get_client_count()
       
        resp_data = {
            'clients_count': clients_count
            }
        
        api_resp['data'] = resp_data
        api_resp['success'] = True
        
    except Exception as err:
        api_resp['success'] = False
        api_resp['error'] = 'Response data error'

    return jsonify(api_resp)



# Информация для панели управления
# общая для админа!
@dashboard.route('/dash/v1.0/dashboard/get_admin_info', methods=['GET'])
@roles_required('admin')
def get_admin_info():
    
    api_resp['url'] = '/dash/v1.0/dashboard/get_admin_info'
    api_resp['method'] = 'GET'
    
    try:
        parsers_count = Parser.query.count()
        moderators_role = Role.query.filter_by(name='moderator').first()
        admins_role = Role.query.filter_by(name='admin').first()
        moderators_count = db.session.query(User).filter(User.roles.contains(moderators_role)).count()
        clients_count = Client.query.count()
        
        clients = Client.query.all()
        parsers = Parser.query.all()
        moderators = db.session.query(User).filter(User.roles.contains(moderators_role)).all()
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'name': user.name,
                'active': user.active,
                'last_login': user.last_login_at,
                'last_logout': user.last_logout_at,
            })
        

        resp_data = {
            'moderators_count': moderators_count,
            'parsers_count': parsers_count,
            'clients_count': clients_count,
            'users': user_list
            }
        
        api_resp['data'] = resp_data
        api_resp['success'] = True
        
    except Exception as err:
        api_resp['success'] = False
        api_resp['error'] = 'Response data error'

    return jsonify(api_resp)



# # Удаление пользователя
# @app.route('/del_user', methods=['POST'])
# @login_required
# def del_user():
    
#     user_id = request.form['id']
#     user = User.query.filter_by(id=user_id).first()
    
#     if user:
#         db.session.delete(user)
#         db.session.commit()
    
#         return jsonify({'status': 'success'})
    
#     else:
#         return jsonify({'status': 'error'})


# # Удаление парсера
# @app.route('/del_parser', methods=['POST'])
# @login_required
# def del_parser():

#     parser_id = request.form['id']
#     parser = Parser.query.filter_by(id=parser_id).first()
    
#     if parser:
#         db.session.delete(parser)
#         db.session.commit()
    
#         return jsonify({'status': 'success'})
    
#     else:
#         return jsonify({'status': 'error'})


# # Добавление нового клиента
# @app.route('/add_client', methods=['POST'])
# @login_required
# def add_client():

#     new_client = Client()
#     new_client.name = request.form['client_name']
#     new_client.generate_key()
#     new_client.generate_sicret()
#     count = request.form['days']
#     new_client.extend_life_marker(count)
    
#     try:
#         db.session.add(new_client)
#         db.session.commit()
#         return jsonify({'status': 'success'})
    
#     except:
#         return jsonify({'status': 'error'})



# @app.route('/api/v1.0/get_last/<count>', methods=['GET'])
# def get_last(count):
    
#     data_list = []
#     data = db.session.query(Data).order_by(Data.id.desc()).limit(count)

#     for item in data:
#         new_item = {
#             'id': item.id,
#             'parser_id': item.parser_id,
#             'datestamp': item.datestamp,
#             'json': item.json
#         }
#         data_list.append(new_item)

#     return jsonify({'result': data_list})


# @app.route('/api/v1.0/set', methods=['POST'])
# def set_data():
    
#     data = request.json
#     result = Parser.query.filter_by(name = data['ID']).first()
    
#     if not result:
#         return jsonify({'status': 'not found parser name'})
    
#     d = Data()
#     d.datestamp = data['datestamp']
#     d.parser_id = data['ID']
#     d.json = str(data['json'])
#     db.session.add(d)
#     db.session.commit() 
    
#     return jsonify({'result': data})