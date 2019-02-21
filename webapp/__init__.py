# -*- coding: utf-8 -*-
import os
import sqlite3

from flask import Flask, render_template, redirect, request, session
from jinja2 import Template

app = Flask(__name__)
app.debug = True


# Get app config from absolute file path
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

DATABASE_PATH=('./database.db')

def connect_db():
    return sqlite3.connect(DATABASE_PATH)

def get_user_from_username_and_password(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f'SELECT id, username FROM `user` WHERE username=\'{username}\' AND password=\'{password}\'')
    row = cur.fetchone()
    conn.commit()
    conn.close()
    return {'id': row[0], 'username': row[1]} if row is not None else None


def get_user_from_id(uid):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT id, username FROM `user` WHERE id=%d' % uid)
    row = cur.fetchone()
    conn.commit()
    conn.close()

    return {'id': row[0], 'username': row[1]}

def render_home_page(uid):
    user = get_user_from_id(uid)
    return render_template('login2.html',user=user)


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'uid' in session:
        return render_home_page(session['uid'])
    return redirect('/login')

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items())
    ))

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      print(request.files)
      f = request.files['file']
      f.save(f.filename)
      return 'file uploaded successfully'

@app.route('/test', methods = ['GET', 'POST'])
def test():
   return render_template('test.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login1.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_from_username_and_password(username, password)
        if user is not None:
            session['uid'] = user['id']
            return redirect('/')
        else:
            return redirect('/login')


@app.route('/logout')
def logout():
    if 'uid' in session:
        session.pop('uid')
    return redirect('/login')

