from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from pymongo import MongoClient

db = SQLAlchemy()
DB_NAME = "database.db"

connection_string = 'mongodb+srv://user:bulletin@cluster0.anxcbeb.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)

housing_db = client.sample_airbnb
housing_collection = housing_db.listingsAndReviews


def create_app():
    app = Flask(__name__,static_url_path='/static', static_folder='static')
    app.config['SECRET_KEY'] = 'Coding Challenge'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .query import query

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(query, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')