from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from sqlalchemy import *
from flask_misaka import Misaka
db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    Misaka(app)
    app.config['SECRET_KEY'] = "pokemon"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User

    create_database(app)

    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME): #verifie si la databese existe, sinon la créé
        with app.app_context():
            db.create_all()
            print('Created Database')
