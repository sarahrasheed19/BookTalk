from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))

class Book(db.Model):
    __tablename__ = 'Book'

    ISBN = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.String(500))
    author = db.Column(db.String(100))
    genre = db.Column(db.String(30))
    tags = db.Column(db.String(200))
