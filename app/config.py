# -*- coding: utf-8 -*-

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = 'das5fgff6h5g4h4d321fsdasdasdayuf78f753'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_TRACKABLE =True        # Flask-security
