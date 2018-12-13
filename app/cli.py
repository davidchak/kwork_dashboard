# -*- coding: utf-8 -*-

import click
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash



def register(app):

    @app.cli.group()
    def system():
        """Translation and localization commands."""
        pass

    @system.command()
    def initdb():
        """Initialize the database."""
        
        from app import db

        db.drop_all()
        db.create_all()

        u1 = app.user_datastore.create_user(name='admin')
        u1.password_hash = generate_password_hash('admin')
        r1 = app.user_datastore.create_role(name='admin')
        u2 = app.user_datastore.create_user(name='moderator')
        u2.password_hash = generate_password_hash('moderator')
        r2 = app.user_datastore.create_role(name='moderator')

        try:
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print('Error: ', err)
        
        app.user_datastore.add_role_to_user(u1, r1)
        app.user_datastore.add_role_to_user(u2, r2)
        
        try:
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print('Error: ', err)
        print('Init DB: Success!')


    @system.command()
    @click.argument('count')
    def remove_data(count):
        from app.models import Data
        data_list = Data.query.all()
        if data_list:
            for data in data_list:
                if data.datestamp >  datetime.now() + timedelta(days=int(count)): 
                    try:
                        db.session.delete(data)
                        db.session.commit()
                    except:
                        db.session.rollback()
                    
        

