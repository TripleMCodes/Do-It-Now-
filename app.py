from flask import Flask, render_template, request, Response, url_for, redirect
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

import logging
logging.basicConfig(level=logging.DEBUG)

db = SQLAlchemy()

def create_app():

    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
    app.secret_key = 'some key'

    bcrypt = Bcrypt(app)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import Users
    @login_manager.user_loader
    def load_user(uid):
        return Users.query.get(uid)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('signup'))

    from routes import app_routes
    app_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app
        
        
