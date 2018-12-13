# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, abort
from . import dashboard
from flask import jsonify, request, current_app
from flask_security import login_required, roles_required, roles_accepted, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Data, User, Parser, Client, Role

# Готово
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

# Готово
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


# Парсер
@dashboard.route('/admin_panel/parsers/<id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def get_parser_data(id):

    parser = Parser.query.filter_by(id = id).first()
    if parser:
        parser_dict = parser.to_dict()
        return render_template('parser.html', parser_dict=parser_dict)
    else:
        abort(404)
        


# Готово
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
# Актив/деактив пользователя              /dash/v1.0/activ_deactiv_user                   - для авторизованного админа
#
# Добавление парсера                      /dash/v1.0/parser/add_parser                    - для авторизованного админа
# Удаление парсера                        /dash/v1.0/parser/del_parser                    - для авторизованного админа
# Получение n-последних записеё парсера   /dash/v1.0/parser/get_last_query/<int>          - для авторизованного админа
#
# Добавление клиента                      /dash/v1.0/client/add_client                    - для авторизованного админа или модератора
# Удаление клиента                        /dash/v1.0/client/del_client                    - для авторизованного админа или модератора
#
# Получение количества зарег.             /dash/v1.0/dashboard/get_admin_counters  - для авторизованного админа
# Получение количества зарег.             /dash/v1.0/dashboard/get_moderator_counters  - для авторизованного админа
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


# Готово
# Добавление пользователя 
@dashboard.route('/dash/v1.0/add_user', methods=['POST'])
@roles_required('admin')
def add_user():

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    username = request.form['login']
    password = request.form['password']
    form_role = request.form['role']

    api_resp['url'] = '/dash/v1.0/add_user'
    api_resp['method'] = 'POST'
    
    unique_test = User.query.filter_by(name = username).first()

    if unique_test:
        api_resp['success'] = False
        api_resp['error'] = 'Такой пользователь уже есть в базе!'
        return jsonify(api_resp)


    user = current_app.user_datastore.create_user(name=username)
    user.password_hash = generate_password_hash(password)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
        api_resp['success'] = False
        api_resp['error'] = 'Ошибка добавления пользователя!'

        return jsonify(api_resp)

    role = Role.query.filter_by(name=form_role).first()
    
    if role:    
        current_app.user_datastore.add_role_to_user(user, role)
        
        try:
            db.session.commit()
        except:
            db.session.rollback()
            api_resp['success'] = False
            api_resp['error'] = 'Ошибка добавления роли пользователю!'
        
            return jsonify(api_resp)

    api_resp['resp_data'] = user.to_dict()
    api_resp['success'] = True
    
    return jsonify(api_resp)


# Готово
# Удаление пользователя 
@dashboard.route('/dash/v1.0/del_user', methods=['POST'])
@roles_required('admin')
def del_user():

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    user_id = request.form['id']

    api_resp['url'] = '/dash/v1.0/del_user'
    api_resp['method'] = 'POST'

    
    user = User.query.filter_by(id=user_id).first()
    if user and user.name != current_user.name:
        try:
            db.session.delete(user)
            db.session.commit()
            api_resp['success'] = True
        except:
            api_resp['success'] = False
            api_resp['error'] = 'Ошибка удаления пользователя!'
    
    return jsonify(api_resp)


# Готово
# Активация/деактивация пользователя 
@dashboard.route('/dash/v1.0/activ_deactiv_user', methods=['POST'])
@roles_required('admin')
def activ_deactiv_user():

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    user_id = request.form['id']

    api_resp['url'] = '/dash/v1.0/activ_deactiv_user'
    api_resp['method'] = 'POST'

    
    user = User.query.filter_by(id=user_id).first()
    if user and user.name != current_user.name:
        user.activ_deactiv_user()
        try:
            db.session.commit()
            api_resp['success'] = True
        except:
            api_resp['success'] = False
            api_resp['error'] = 'Ошибка активации/деактивации пользователя'
    else:
        api_resp['success'] = False
        api_resp['error'] = "Текущий пользователь не может быть деактивирован!"

    return jsonify(api_resp)


# Готово
# Добавление парсера 
@dashboard.route('/dash/v1.0/add_parser', methods=['POST'])
@roles_required('admin')
def add_parser():
    

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }


    parser_name = request.form['name']

    api_resp['url'] = '/dash/v1.0/add_parser'
    api_resp['method'] = 'POST'

    unique_test = Parser.query.filter_by(name = parser_name).first()

    if unique_test:
        api_resp['success'] = False
        api_resp['error'] = 'Парсер с таким именем уже есть в базе!'
        
        return jsonify(api_resp)

    new_parser = Parser(name=parser_name)
    new_parser.get_token()

    try:
        db.session.add(new_parser)
        db.session.commit()
        api_resp['success'] = True
    except Exception as err:
        api_resp['success'] = False
        api_resp['error'] = err
        return jsonify(api_resp)

    api_resp['resp_data'] = new_parser.to_dict()
    
    return jsonify(api_resp)


# Готово
# Удаление парсера 
@dashboard.route('/dash/v1.0/del_parser', methods=['POST'])
@roles_required('admin')
def del_parser():

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }


    parser_id = request.form['id']

    api_resp['url'] = '/dash/v1.0/del_parser'
    api_resp['method'] = 'POST'

    
    parser = Parser.query.filter_by(id=parser_id).first()
    if parser:
        try:
            db.session.delete(parser)
            db.session.commit()
            api_resp['success'] = True
        except:
            api_resp['success'] = False
            api_resp['error'] = 'Ошибка удаления парсера!'
    
    return jsonify(api_resp)


# Готово
# Добавление клиента 
@dashboard.route('/dash/v1.0/add_client', methods=['POST'])
@roles_accepted('moderator', 'admin')
def add_client():

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    name = request.form['name']

    api_resp['url'] = '/dash/v1.0/add_client'
    api_resp['method'] = 'POST'
    
    new_client = Client(name=name)
    new_client.user = current_user
    new_client.get_token()
    
    try:
        db.session.add(new_client)
        db.session.commit()
        api_resp['success'] = True
        api_resp['resp_data'] = new_client.to_dict()
    except:
        api_resp['error'] = 'Ошибка добавления клиента!'
        return jsonify(api_resp)
    
    api_resp['success'] = True
    
    return jsonify(api_resp)


# Готово
# Удаление клиента 
@dashboard.route('/dash/v1.0/del_client', methods=['POST'])
@roles_accepted('admin', 'moderator')
def del_client():

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    cleint_id = request.form['id']

    api_resp['url'] = '/dash/v1.0/del_client'
    api_resp['method'] = 'POST'

    
    client = Client.query.filter_by(id=cleint_id).first()
    if client:
        try:
            db.session.delete(client)
            db.session.commit()
            api_resp['success'] = True
        except:
            api_resp['success'] = False
            api_resp['error'] = 'Ошибка удаления клиента!'
    
    return jsonify(api_resp)


# Готово
# Продление токена клиента 
@dashboard.route('/dash/v1.0/update_client_token', methods=['POST'])
@roles_accepted('admin', 'moderator')
def update_client_token():

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    cleint_id = request.form['id']
    count = request.form['count']

    api_resp['url'] = '/dash/v1.0/update_client_token'
    api_resp['method'] = 'POST'

    client = Client.query.filter_by(id=cleint_id).first()
    print(client.name)
    if client:
        client.update_token_expiration(int(count))
        try:
            db.session.commit()
            api_resp['success'] = True
            api_resp['resp_data'] = {'token_expiration': client.token_expiration}
        except:
            api_resp['success'] = False
            api_resp['error'] = 'Ошибка продления токена!'
    
    return jsonify(api_resp)


# Готово
# Активация/деактивация клиента 
@dashboard.route('/dash/v1.0/activ_deactiv_client', methods=['POST'])
@roles_required('moderator')
def activ_deactiv_client():

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    client_id = request.form['id']

    api_resp['url'] = '/dash/v1.0/activ_deactiv_user'
    api_resp['method'] = 'POST'

    
    client = Client.query.filter_by(id=client_id).first()
    if client:
        client.activ_deactiv_client()
        try:
            db.session.commit()
            api_resp['success'] = True
        except:
            api_resp['success'] = False
            api_resp['error'] = 'Ошибка активации/деактивации клиента'

    return jsonify(api_resp)


# Готово
# Получение счетчиков для модератора
@dashboard.route('/dash/v1.0/get_moderator_counters', methods=['GET'])
@roles_required('moderator')
def get_moderator_counters():

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    api_resp['url'] = '/dash/v1.0/get_moderator_counters'
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


# Готово
# Получение счетчиков для админа
@dashboard.route('/dash/v1.0/get_admin_counters', methods=['GET'])
@roles_required('admin')
def get_admin_counters():
    
    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    api_resp['url'] = '/dash/v1.0/get_admin_counters'
    api_resp['method'] = 'GET'
    
    try:
        parsers_count = Parser.query.count()
        moderators_role = Role.query.filter_by(name='moderator').first()
        admins_role = Role.query.filter_by(name='admin').first()
        admins_count = db.session.query(User).filter(User.roles.contains(admins_role)).count()
        moderators_count = db.session.query(User).filter(User.roles.contains(moderators_role)).count()
        clients_count = Client.query.count()
        

        resp_data = {
            'moderators_count': moderators_count,
            'parsers_count': parsers_count,
            'clients_count': clients_count,
            'admins_count': admins_count
        }
        
        api_resp['data'] = resp_data
        api_resp['success'] = True
        
    except Exception as err:
        api_resp['success'] = False
        api_resp['error'] = 'Ошибка получения счетчиков'

    return jsonify(api_resp)


    #     clients = Client.query.all()
    #     parsers = Parser.query.all()
    #     moderators = db.session.query(User).filter(User.roles.contains(moderators_role)).all()
    #     users = User.query.all()
    #     user_list = []
    #     for user in users:
    #         user_list.append({
    #             'id': user.id,
    #             'name': user.name,
    #             'active': user.active,
    #             'last_login': user.last_login_at,
    #             'last_logout': user.last_logout_at,
    #         })
        

    #     resp_data = {
    #         'moderators_count': moderators_count,
    #         'parsers_count': parsers_count,
    #         'clients_count': clients_count,
    #         'users': user_list
    #         }
        
    #     api_resp['data'] = resp_data
    #     api_resp['success'] = True
        
    # except Exception as err:
    #     api_resp['success'] = False
    #     api_resp['error'] = 'Response data error'

    # return jsonify(api_resp)



