# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect
from flask_security import login_required, roles_required, current_user
from . import dashboard


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

    return render_template('admin.html')


# Модераторка
@dashboard.route('/moderator_panel/<username>', methods=['GET', 'POST'])
@login_required
@roles_required('moderator')
def get_moderator_page(username):
    
    return render_template('moderator.html')