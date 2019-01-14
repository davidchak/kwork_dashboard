# -*- coding: utf-8 -*-

from flask import jsonify, request, current_app, g
from flask_security import login_required, roles_required, roles_accepted, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import api
from app import db
from app.models import Data, User, Parser, Client, Role
from .auth import client_token_auth, parser_token_auth, users_basic_auth
from datetime import datetime


###############################################################################################################
#                                           Client API                                                        #
###############################################################################################################
@api.route('/api/v1.0/clients/get_data/<int:count>', methods=['GET'])
@client_token_auth.login_required
def get_client_data(count):
    

    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    api_resp['url'] = '/api/v1.0/clients/get_data/<count>'
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
    api_resp['resp_data'] = data_list

    return jsonify(api_resp)


###############################################################################################################
#                                           Parser API                                                        #
###############################################################################################################
@api.route('/api/v1.0/parsers/set_data', methods=['POST'])
@parser_token_auth.login_required
def set_parser_data():

    format = r"%Y-%m-%d %H:%M:%S"
    
    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    data = request.json


    api_resp['url'] = '/api/v1.0/parsers/set_data'
    api_resp['method'] = 'POST'

    parser = Parser.query.filter_by(token=data['token']).first()

    if parser:
        parser.set_data(datestamp=datetime.strptime(data['datestamp'][:-7], format), json=str(data['json']))
        api_resp['success'] = True
    else:
        api_resp['success'] = False

    return jsonify(api_resp)


###############################################################################################################
#                                           User API                                                          #
###############################################################################################################
#  +  /api/v1.0/help                     GET       root, admin, moderator                                                 #
#  +  /api/v1.0/users/get                GET       root, admin                                                 #
#  +  /api/v1.0/users/add                POST      root, admin                                                 #
#  +  /api/v1.0/users/del                POST      root, admin                                                 #
#  +  /api/v1.0/clients/get              GET       root, admin, moderator                                      #
#  +  /api/v1.0/clients/add              POST      root, admin, moderator                                      #
#  +  /api/v1.0/clients/del              POST      root, admin, moderator                                      #
#     /api/v1.0/clients/prolong          POST      root, admin, moderator                                      #
#  +  /api/v1.0/parsers/get              GET       root, admin                                                 #
#  +  /api/v1.0/parsers/add              POST      root, admin                                                 #
#  +  /api/v1.0/parsers/del              POST      root, admin                                                 #
###############################################################################################################
#    response_data = {                                                                                        #
#       'api': '/api/v1.0/users/',                                                                            #
#       'method': 'get/post',                                                                                 #
#       'success': True/False,                                                                                #
#       'data': data object,
#       'error': error str                                                                                        #
# }                                                                                                           #
###############################################################################################################

# Получить пользователей
@api.route('/api/v1.0/help', methods=['GET'])
@users_basic_auth.login_required
def get_help():
    resp_data = {}
    resp_data['api'] = '/api/v1.0/help'
    resp_data['method'] = 'get'
    resp_data['data'] = {
        'routes': [
            { 'url': '/api/v1.0/help', 'description':'Справка', 'method':'GET', 'access':'root, admin, moderator'},
            { 'url': '/api/v1.0/users/get','description':'Получить пользователей', 'method': 'GET', 'access': 'root, admin'},
            { 'url': '/api/v1.0/users/add','description':'Добавить пользователя, принимает параметры: name', 'method': 'POST', 'access': 'root, admin'},
            {'url': '/api/v1.0/users/del', 'description': 'Удалить пользователей, принимает параметры: id или token',
                'method': 'POST', 'access': 'root, admin'},
            { 'url': '/api/v1.0/clients/get', 'description':'Получить клиентов', 'method': 'POST','access': 'root, admin'},
            { 'url': '/api/v1.0/clients/add','description':'Добавить клиента, принимает параметры: name', 'method':'GET', 'access':'root, admin, moderator'},
            {'url': '/api/v1.0/clients/del ', 'description': 'Удалить клиента, принимает параметры: id или token',
                'method': 'GET', 'access': 'root, admin, moderator'},
            {'url': '/api/v1.0/clients/prolong', 'description': 'Продлить токен клиента, принимает параметры: id или token и days(количество дней)',
                'method': 'GET', 'access': 'root, admin, moderator'},
            { 'url': '/api/v1.0/parsers/get','description':'Получить парсеры', 'method':'GET', 'access':'root, admin'},
            {'url': '/api/v1.0/parsers/add', 'description': 'Добавить парсер, принимает параметры: name',
                'method': 'GET', 'access': 'root, admin'},
            {'url': '/api/v1.0/parsers/del', 'description': 'Удалить парсер , принимает параметры: id или token',
                'method': 'GET', 'access': 'root, admin'}
        ]
    }
    resp_data['error'] = ''
    return jsonify(resp_data)


# Получить пользователей
@api.route('/api/v1.0/users/get', methods=['GET'])
@users_basic_auth.login_required
def get_users():
    resp_data = {}
    resp_data['api'] = '/api/v1.0/users/get'                                                                          
    resp_data['method'] = 'get'
    resp_data['data'] = []
    resp_data['error'] = ''
    
    if g.user.has_role('root'):
        users = User.query.all()
        for user in users:
            resp_data['data'].append(user.to_dict())
        resp_data['success'] = True


    elif g.user.has_role('admin'):
        users = User.query.filter_by(parent_id=g.user.id).all()
        for user in users:
            resp_data['data'].append(user.to_dict())
        resp_data['success'] = True

    else:
        resp_data['success'] = False

    return jsonify(resp_data)


# Создание пользователей
@api.route('/api/v1.0/users/add', methods=['POST'])
@users_basic_auth.login_required
def add_user():  
    
    resp_data = {}
    resp_data['api'] = '/api/v1.0/users/add'                                                                          
    resp_data['method'] = 'post'
    resp_data['data'] = [] 
    resp_data['error'] = ''  
        
    data = request.json

    if not data.has_key('name') or not data.has_key('password') or not data.has_key('role'): 
        resp_data['error'] = 'Нет одного или нескольких параметров: name, password, role'
        return jsonify(resp_data)

    if g.user.has_role('admin') and data['role'] == 'admin':
        resp_data['error'] = 'Администратор не может создавать пользователей с ролью admin!'
        return jsonify(resp_data)

    if g.user.has_role('moderator'):
        resp_data['error'] = 'Модератор не может создавать пользователей!'
        return jsonify(resp_data)

    unique_test = User.query.filter_by(name=data['name']).first()

    if unique_test:
        resp_data['success'] = False
        resp_data['error'] = 'Указанный пользователь уже есть в базе!'
        return jsonify(resp_data)

    user = current_app.user_datastore.create_user(name=data['name'])
    user.password_hash = generate_password_hash(data['password'])
    user.parent_id = g.user.id

    try:
        db.session.commit()
    except:
        db.session.rollback()
        resp_data['success'] = False
        resp_data['error'] = 'Ошибка добавления пользователя!'

        return jsonify(resp_data)

    role = Role.query.filter_by(name=data['role']).first()

    if role:
        current_app.user_datastore.add_role_to_user(user, role)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            resp_data['success'] = False
            resp_data['error'] = 'Ошибка добавления роли пользователю!'

            return jsonify(resp_data)

    resp_data['data'] = user.to_dict()
    resp_data['success'] = True

    return jsonify(resp_data)
    


# Удаление пользователей
@api.route('/api/v1.0/users/del', methods=['POST'])
@users_basic_auth.login_required
def del_user():

    resp_data = {}
    resp_data['api'] = '/api/v1.0/users/del'
    resp_data['method'] = 'post'
    resp_data['data'] = []
    resp_data['error'] = ''

    # получаем данные для удаления
    data = request.json

    if data.has_key('id'):
        user = User.query.filter_by(id=data['id']).first()
    elif data.has_key('id'):
        user = User.query.filter_by(name=data['name']).first()
    else:
        resp_data['success'] = False
        resp_data['error'] = 'Необходимо передать параметр id или name!'
        return jsonify(resp_data)

    # если пользователя в базе нет - ошибка
    if user is None:
        resp_data['error'] = 'Пользователь не найден в базе!'
        return jsonify(resp_data)

    # если тот кто удаляет не root и учетка не удаляет сама себя
    if g.user.name != 'root' and user.parent_id != g.user.id:
        resp_data['error'] = 'Ошибка удаления пользователя!'
        return jsonify(resp_data)


    
    moderators = User.query.filter_by(parent_id=user.id).all()
    if moderators:
        for moderator in moderators:
            clients = Client.query.filter_by(user_id=moderator.id).all()
            if clients:
                for client in clients:
                    try:
                        db.session.delete(client)
                        db.session.commit()
                    except:
                        resp_data['error'] = 'Не удалось удалить клиентов удаляемого пользователя!'
                        return jsonify(resp_data)
            try:
                db.session.delete(moderator)
                db.session.commit()
            except:
                resp_data['error'] = 'Не удалось удалить засисимых пользователей удаляемого пользователя!'
                return jsonify(resp_data)
    
    parsers = Parser.query.filter_by(user_id=user.id).all()
    if parsers:
        for parser in user.parsers:
            try:
                db.session.delete(parser)
                db.session.commit()
            except:
                resp_data['error'] = 'Не удалось удалить парсеры удаляемого пользователя!'
                return jsonify(resp_data)
    
    clients = Client.query.filter_by(user_id=user.id).all()
    if clients:
        for client in clients:
            try:
                db.session.delete(client)
                db.session.commit()
            except:
                db.session.rollback()
                resp_data['error'] = 'Ошибка удаления клиента удаляемого пользователя!'
                return jsonify(resp_data)

    try:
        db.session.delete(user)
        db.session.commit()
        resp_data['success'] = True
    except:
        db.session.rollback()
        resp_data['error'] = 'Ошибка удаления пользователя!'

    return jsonify(resp_data)


# Получить парсеры
@api.route('/api/v1.0/parsers/get', methods=['GET'])
@users_basic_auth.login_required
def get_parsers():
    resp_data = {}
    resp_data['api'] = '/api/v1.0/parsers/get'
    resp_data['method'] = 'get'
    resp_data['data'] = []
    resp_data['error'] = ''

    if g.user.has_role('root'):
        parsers = Parser.query.all()
        for parser in parsers:
            resp_data['data'].append(parser.to_dict())
        resp_data['success'] = True

    elif g.user.has_role('admin'):
        parsers = Parser.query.filter_by(user_id=g.user.id).all()
        for parser in parsers:
            resp_data['data'].append(parser.to_dict())
        resp_data['success'] = True

    else:
        resp_data['success'] = False

    return jsonify(resp_data)


# Добавить парсер
@api.route('/api/v1.0/parsers/add', methods=['POST'])
@users_basic_auth.login_required
def add_parser():
    resp_data = {}
    resp_data['api'] = '/api/v1.0/parsers/add'
    resp_data['method'] = 'post'
    resp_data['data'] = []
    resp_data['error'] = ''

    data = request.json
    
    if g.user.has_role('moderator'):
        resp_data['error'] = 'Ошибка добавления парсера!'
        return jsonify(resp_data)
   
    new_parser = Parser(name=data['name'])
    new_parser.owner = g.user
    new_parser.get_token()

    try:
        db.session.add(new_parser)
        db.session.commit()
        resp_data['success'] = True
        resp_data['data'] = new_parser.to_dict()
    except:
        resp_data['error'] = 'Ошибка добавления клиента!'
        return jsonify(resp_data)

    return jsonify(resp_data)


# Удалить парсер
@api.route('/api/v1.0/parsers/del', methods=['POST'])
@users_basic_auth.login_required
def del_parser():
    resp_data = {}
    resp_data['api'] = '/api/v1.0/parsers/del'
    resp_data['method'] = 'post'
    resp_data['data'] = []
    resp_data['error'] = ''

    data = request.json

    if g.user.has_role('moderator'):
        resp_data['error'] = 'Ошибка удаления парсера!'
        return jsonify(resp_data)

    if data.has_key('id'):
        parser = Parser.query.filter_by(id=data['id']).first()
    elif data.has_key('token'):
        parser = Parser.query.filter_by(token=data['token']).first()

    if parser is None:
        resp_data['success'] = False
        resp_data['error'] = 'Парсер не обнаружен!'
        return jsonify(resp_data)
    
    if parser.owner == g.user or g.user.has_role('root'): 
        try:
            db.session.delete(parser)
            db.session.commit()
            resp_data['success'] = True
        except:
            resp_data['error'] = 'Ошибка удаления парсера!'
            return jsonify(resp_data)

    return jsonify(resp_data)


# Получить клиентов
@api.route('/api/v1.0/clients/get', methods=['GET'])
@users_basic_auth.login_required
def get_clients():
    resp_data = {}
    resp_data['api'] = '/api/v1.0/clients/get'
    resp_data['method'] = 'get'
    resp_data['data'] = []
    resp_data['error'] = ''

    if g.user.has_role('root'):
        clients = Client.query.all()
        for client in clients:
            resp_data['data'].append(client.to_dict())
        resp_data['success'] = True

    elif g.user.has_role('admin'):
        users = User.query.filter_by(parent_id=g.user.id).all()
        clients = Client.query.all()
        for client in clients:
            if client.owner in users:
                resp_data['data'].append(client.to_dict())
        resp_data['success'] = True

    elif g.user.has_role('moderator'):
        clients = Client.query.filter_by(user_id=g.user.id).all()
        for client in clients:
            resp_data['data'].append(client.to_dict())
        resp_data['success'] = True

    else:
        resp_data['success'] = False

    return jsonify(resp_data)


# Добавить клиента
@api.route('/api/v1.0/clients/add', methods=['POST'])
@users_basic_auth.login_required
def add_client():

    resp_data = {}
    resp_data['api'] = '/api/v1.0/clients/add'
    resp_data['method'] = 'post'
    resp_data['data'] = []
    resp_data['error'] = ''

    data = request.json

    if data is None:
        resp_data['success'] = False
        resp_data['error'] = 'Необходимо передать имя клиента параметром name'
        return jsonify(resp_data)

    new_client = Client(name=data['name'])
    new_client.owner = g.user
    new_client.get_token()

    try:
        db.session.add(new_client)
        db.session.commit()
        resp_data['success'] = True
        resp_data['data'] = new_client.to_dict()
    except:
        resp_data['error'] = 'Ошибка добавления клиента!'
        return jsonify(resp_data)

    return jsonify(resp_data)


# Удаление клиента
@api.route('/api/v1.0/clients/del', methods=['POST'])
@users_basic_auth.login_required
def del_client():

    resp_data = {}
    resp_data['api'] = '/api/v1.0/clients/del'
    resp_data['method'] = 'post'
    resp_data['data'] = []
    resp_data['error'] = ''

    data = request.json

    if data.has_key('token'):
        client = Client.query.filter_by(token=data['token']).first()
    elif data.has_key('id'):
        client = Client.query.filter_by(id=data['id']).first()

    if not g.user.has_role('root') and g.user != client.owner:
        resp_data['error'] = 'Ошибка удаления клиента!'
        return jsonify(resp_data)

    try:
        db.session.delete(client)
        db.session.commit()
        resp_data['success'] = True
    except:
        resp_data['error'] = 'Ошибка удаления клиента!'
        return jsonify(resp_data)

    return jsonify(resp_data)


# Продлить токен клиента
@api.route('/api/v1.0/clients/prolong', methods=['POST'])
@users_basic_auth.login_required
def prolong_client_token():
    resp_data = {}
    resp_data['api'] = '/api/v1.0/clients/prolong'
    resp_data['method'] = 'post'
    resp_data['data'] = []
    resp_data['error'] = ''

    data = request.json

    if not data.has_key('days'):
        resp_data['success'] = False
        resp_data['error'] = '1. Не указано количество дней для продления!'
        return jsonify(resp_data)

    if data.has_key('id'):
        client = Client.query.filter_by(id=data['id']).first()
    elif data.has_key('token'):
        client = Client.query.filter_by(token=data['token']).first()
    else:
        resp_data['success'] = False
        resp_data['error'] = '2. Необходиме передать id или token клиента!'
        return jsonify(resp_data)

    if client is None:
        resp_data['success'] = False
        resp_data['error'] = '3. Объект не найден!'
        return jsonify(resp_data)

    if not g.user.has_role('root') and client.owner != g.user:
        resp_data['success'] = False
        resp_data['error'] = '4. Нужно быть владельцем или root для удаления!'
        return jsonify(resp_data)
        
    try:
        client.update_token_expiration(int(data['days']))
        db.session.commit()
        resp_data['data'] = client.to_dict()
        resp_data['success'] = True
    except:
        resp_data['success'] = False
        resp_data['error'] = '5. Ошибка продления токена клиента!'
        return jsonify(resp_data)

    return jsonify(resp_data)
