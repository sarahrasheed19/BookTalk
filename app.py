from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from eBookClub import settings

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = settings.MYSQL_URI
app.config['SECRET_KEY'] = settings.SECRETKEY

db = SQLAlchemy(app)

engine = create_engine(settings.MYSQL_URI)
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
        self.cover = cover

class ForumPosts(db.Model):
    __tablename__ = "ForumPosts"

    postID = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('Posts.user_id'))
    ISBN = db.Column(db.String(30), db.ForeignKey('Posts.book_isbn'))

# setting up flask-security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('user_home.html')

@app.route('/bookclub')
def bookclub():
    return render_template('bookclub_home_public.html')

@app.route('/mybookclub')
def mybookclub():
    return render_template('bookclub_home_member.html')

@app.route('/settings')
def settings():
    return render_template('user_settings.html')

@app.route('/forums')
def forums():
    return render_template('bookclub_forums.html')

@app.route('/registerauth', methods=['POST','GET'])
def register():
    if request.method=='POST':
       # user_datastore.create_user( email = request.form.get('inputEmail') , password = request.form.get('inputPassword'))
       # db.session.commit()
        return redirect('/home')
    return render_template('index.html')
 # Route for handling the login page logic
@app.route('/loginauth', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form["inputEmail"] != 'admin@admin.com' or request.form["inputPassword"] != 'admin':
            error = 'Invalid username or password'
        else:
            return redirect('/home')
    return render_template('index.html', error=error)
