# -*- coding: utf-8 -*-

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'das5fgff6h5g4h4d321fsdasdasdayuf78f753'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_TRACKABLE =True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SECURITY_TRACKABLE = True
    REMEMBER_COOKIE_DURATION = 3600
