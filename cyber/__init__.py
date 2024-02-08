from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'd85881b468478b095e061c02700bf467'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../lamport.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from cyber import routes
