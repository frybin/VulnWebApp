from webapp import *


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'uid' in session:
        return render_template('uploadlock.html',flag=FLAG,hash=FLAG2HASH,url_flag=url_for('flag', _external=True),url_upload=url_for('upload_file', _external=True))
    return redirect('/login')

@app.route('/uploader', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      if('.zip' in f.filename):
          extract_path=os.path.join(os.path.dirname(os.path.realpath(__file__)))
          save_file=(extract_path+'/'+f.filename)
          f.save(save_file)
          unzip(save_file,extract_path)
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