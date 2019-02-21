# -*- coding: utf-8 -*-
import os
import io
import sqlite3
import zipfile
import hashlib
from flask import Flask, render_template, redirect, request, session
from jinja2 import Template
from config import settings

app = Flask(__name__)
app.debug = True

app.config.from_object('config.settings')
DATABASE_PATH=('./database.db')
FLAG = os.environ.get("FLAG", default='Not Set')
FLAG2 = os.environ.get("FLAG2", default='Not Set')
FLAG2PASS=os.environ.get("FLAG2PASS", default='test')
FLAG2HASH=hashlib.sha1(FLAG2PASS.encode('utf-8')).hexdigest()

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

def unzip(zip_file, extraction_path):
    """
    code to unzip files
    """
    print("[INFO] Unzipping")
    try:
        files = []
        with zipfile.ZipFile(zip_file, "r") as z:
            for fileinfo in z.infolist():
                filename = fileinfo.filename
                dat = z.open(filename, "r")
                files.append(filename)
                outfile = os.path.join(extraction_path, filename)
                if not os.path.exists(os.path.dirname(outfile)):
                    try:
                        os.makedirs(os.path.dirname(outfile))
                    except OSError as exc:  # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            print ("\n[WARN] OS Error: Race Condition")
                if not outfile.endswith("/"):
                    with io.open(outfile, mode='wb') as f:
                        f.write(dat.read())
                dat.close()
        return files
    except Exception as e:
        print ("[ERROR] Unzipping Error" + str(e))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'uid' in session:
        return render_template('uploadlock.html',flag=FLAG,hash=FLAG2HASH)
    return redirect('/login')

@app.route('/uploader', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      if('.zip' in f.filename):
          save_file=("./uploads/"+f.filename)
          f.save(save_file)
          unzip(save_file,'./uploads')
          print('file uploaded successfully')
      return 'file uploaded successfully'

@app.route('/flag', methods = ['GET', 'POST'])
def flag():
    if 'uid' in session:
        password=request.args['pass']
        if(password==FLAG2PASS):
            return render_template('flag2.html',flag2=FLAG2)
    return redirect('/')

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

