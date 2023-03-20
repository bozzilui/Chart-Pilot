from flask import Flask
import dash
from dash import dcc, html
from flask_sqlalchemy import SQLAlchemy
from website.dashapp import layout
from os import path
from flask_login import LoginManager
import dash_bootstrap_components as dbc
import dash_html_components as html

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app_dash = dash.Dash(__name__, server=app,external_stylesheets=[dbc.themes.CYBORG], url_base_pathname='/dashboard/')
    app_dash.layout = layout.dashboard("MSFT")
    app_dash.title = "Dashboard"
    app.config['SECRET_KEY'] = 'hello'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return (app, app_dash)

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

