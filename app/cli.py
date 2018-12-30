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
    @click.argument('passwd')
    def initdb(passwd):
        """Initialize the database."""
        
        from app import db

        db.drop_all()
        db.create_all()

        u0 = app.user_datastore.create_user(name='root')
        u0.password_hash = generate_password_hash(passwd)
        
        r0 = app.user_datastore.create_role(name='root')
        r1 = app.user_datastore.create_role(name='admin')
        r2 = app.user_datastore.create_role(name='moderator')

        try:
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print('Error: ', err)
            
        u0.parent_id = u0.id
        app.user_datastore.add_role_to_user(u0, r0)
     
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
                    
        

