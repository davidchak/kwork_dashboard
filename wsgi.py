# -*- coding: utf-8 -*-

from app import create_app, db
from app.models import Client, Data, Parser, Role, User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Client': Client, 'Data': Data,
            'Parser': Parser, 'Role': Role}


if __name__ == '__main__':
    app.run(debug=True)