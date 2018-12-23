# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, abort
from . import dashboard
from flask import jsonify, request, current_app
from flask_security import login_required, roles_required, roles_accepted, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Data, User, Parser, Client, Role



#####################################################################################################
#   URL                     Описание                Права доступа                      Метод        #
#---------------------------------------------------------------------------------------------------#
#   /root/<id>          - Главный юзер              root                               GET          #
#   /admin/<id>         - Администратор             root, admin                        GET          #
#   /moderator/<id>     - Модератор                 root, admin, moderator             GET          #
#   /client/<id>        - Клиент                    root, admin, moderator, client     GET          #
#   /parser/<id>        - Парсер                    root, admin                        GET          #
#                                                                                                   #
#####################################################################################################

@dashboard.route('/', methods=['GET'])
@login_required
def get_index_page():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard.get_user_page', id=current_user.id))
    else:
        return redirect(url_for('auth.login'))


# Страница пользоватлея
@dashboard.route('/user/<id>', methods=['GET'])
@login_required
@roles_accepted('root', 'admin', 'moderator')
def get_user_page(id):

    if current_user.has_role('root'):
        
        users = User.query.all()
        parsers = Parser.query.all()
        clients = Client.query.all()
        # clients_count = Client.query.count()
        # parsers_count = Parser.query.count()
        # admins_role = Role.query.filter_by(name='admin').first()
        # admins_count = db.session.query(User).filter(User.roles.contains(admins_role)).count()
        # moderators_role = Role.query.filter_by(name='moderator').first()
        # moderators_count = db.session.query(User).filter(User.roles.contains(moderators_role)).count()

        return render_template('common.html', users=users, parsers=parsers, clients=clients)
    
    elif current_user.has_role('admin'):
        users = User.query.filter_by(parent_id = current_user.id).all()
        parsers = Parser.query.filter_by(parent_id = current_user.id).all()
        # return render_template('common.html', users=users, parsers=parsers, clients=clients)
        return render_template('common.html', users=users, parsers=parsers)
    
    elif current_user.has_role('moderator'):
        # return render_template('common.html', clients=clients)
        return render_template('common.html')
    
    else:
        abort(404)


# Страница парсера
@dashboard.route('/parser/<id>', methods=['GET'])
@login_required
@roles_accepted('root', 'admin', 'moderator')
def get_parser_page(id):

    parser = Parser.query.filter_by(id = id).first()

    if parser:
        parser_dict = parser.to_dict(current_user.id)
    
        if parser_dict is not None:
            return render_template('parser.html', parser_dict=parser_dict)
        else:
            abort(404)
    else:
        abort(404)

#####################################################################################################
#                                           ERRORS PAGE                                             #
#####################################################################################################

@dashboard.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@dashboard.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500



#####################################################################################################
#                                           DASH API                                                #
#####################################################################################################

@dashboard.route('/dash/v1.0/add_user', methods=['POST'])
@roles_accepted('moderator', 'admin', 'root')
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
    user.parent_id = current_user.id
    
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


@dashboard.route('/dash/v1.0/del_user', methods=['POST'])
@roles_accepted('root', 'admin')
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


@dashboard.route('/dash/v1.0/activ_deactiv_user', methods=['POST'])
@roles_accepted('root', 'admin')
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


@dashboard.route('/dash/v1.0/add_parser', methods=['POST'])
@roles_accepted('root', 'admin')
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
    new_parser.parent_id = current_user.id

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


@dashboard.route('/dash/v1.0/del_parser', methods=['POST'])
@roles_accepted('root', 'admin')
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


@dashboard.route('/dash/v1.0/add_client', methods=['POST'])
@roles_accepted('moderator', 'admin', 'root')
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
    new_client.parent_id = current_user.parent_id
    
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


@dashboard.route('/dash/v1.0/del_client', methods=['POST'])
@roles_accepted('moderator', 'admin', 'root')
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


@dashboard.route('/dash/v1.0/update_client_token', methods=['POST'])
@roles_accepted('moderator', 'admin', 'root')
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


@dashboard.route('/dash/v1.0/get_root_counters', methods=['GET'])
@roles_required('root')
def get_root_counters():
    
    api_resp = {
        'url': '',     
        'method': '',                 
        'success': True,                 
        'resp_data': '',               
        'error': ''                
    }

    api_resp['url'] = '/dash/v1.0/get_root_counters'
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