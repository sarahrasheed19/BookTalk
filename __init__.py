from . import settings

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = settings.MYSQL_URI
app.config['SECRET_KEY'] = settings.SECRETKEY

db = SQLAlchemy(app) 
