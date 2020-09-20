from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore,
from eBookClub import settings
from models import User, Role

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = settings.MYSQL_URI
app.config['SECRET_KEY'] = settings.SECRETKEY
db = SQLAlchemy(app)

user_datastore=SQLAlchemyUserDatastore(db, 'User', 'Role')
security=Security(app,user_datastore)

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method=='POST':
        user_datastore.create_user( email = request.form.get('email') , password = request.form.get('password'))
        db.session.commit()


        return redirect(url_for('home'))

    return render_template('register.html')


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid username or password'
        else:
            return redirect(url_for('home'))
    return render_template('index.html', error=error)

@app.route('/home')

def home():
    return render_template('user_home.html')
