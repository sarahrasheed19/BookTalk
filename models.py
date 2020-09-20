from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import MYSQL_URI
from app import app, db

engine = create_engine(MYSQL_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

role_users = db.Table('role_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
    extend_existing = True)

Posts = db.Table('Posts',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('book_isbn', db.String(30), db.ForeignKey('Book.ISBN')))

class Role(db.Model, RoleMixin):
    __tablename__ = 'Role'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, db.ForeignKey('role_users.role_id'), primary_key=True)
    role_name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, role_name, description):
        self.role_name = role_name
        self.description = description


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer, db.ForeignKey('role_users.user_id'), primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), nullable=False)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    roles = db.relationship('Role', secondary=role_users, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, password, fname, lname):
        self.email = email
        self.password = password
        self.fname = fname
        self.lname = lname

class Book(db.Model):
    __tablename__ = 'Book'

    ISBN = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.String(500))
    author = db.Column(db.String(100))
    genre = db.Column(db.String(30))
    tags = db.Column(db.String(200))
    cover = db.Column(db.BLOB)

    def __init__(self, ISBN, title, author, genre, tags, cover):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.genre = genre
        self.tags = tags
        self.cover

class ForumPosts(db.Model):
    __tablename__ = "ForumPosts"

    postID = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('Posts.user_id'))
    ISBN = db.Column(db.String(30), db.ForeignKey('Posts.book_isbn'))
