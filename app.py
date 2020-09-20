from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from eBookClub import settings
from eBookClub.models import user_datastore, security 
from eBookClub import app

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
