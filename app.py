import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from werkzeug.utils import secure_filename
from dataProcessing import *
from Threads import *
from flask import send_file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import time
import os
import re
script = ''

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['txt'])

# api = API(app)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["CACHE_TYPE"] = "null"
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Quick@867'
app.config['MYSQL_DB'] = 'geeklogin'
 
mysql = MySQL(app)

def resultE():
    path = "./Segments"
    dir_list = os.listdir(path)
    print(dir_list)
    return render_template('Result.html',dir_list = dir_list)

def resultD():
    return render_template('resultD.html')

@app.route('/encrypt/')
def EncryptInput():
  Segment()
  gatherInfo()
  HybridCrypt()
  return resultE()

@app.route('/decrypt/')
def DecryptMessage():
  st=time.time()
  HybridDeCrypt()
  et=time.time()
  print(et-st)
  trim()
  st=time.time()
  Merge()
  et=time.time()
  print(et-st)
  return resultD()

def start():
  content = open('./Original.txt','r')
  content.seek(0)
  first_char = content.read(1) 
  if not first_char:
    return render_template('Empty.html')
  else:
    return render_template('Option.html')
  

@app.route('/go_back_home')
def go_back_home():
    return render_template('home.html')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/team')
def team():
  return render_template('team.html')

@app.route('/loginpage')
def loginpage():
  return render_template('loginpage.html')

@app.route('/aboutmore')
def aboutmore():
  return render_template('aboutmore.html')

@app.route('/AES')
def AES():
  return render_template('AES.html')

@app.route('/BLOWFISH')
def BLOWFISH():
  return render_template('BLOWFISH.html')


@app.route('/DES')
def DES():
  return render_template('DES.html')

@app.route('/cybersecurity')
def cybersecurity():
  return render_template('cybersecurity.html')

@app.route('/privacypolicy')
def privacypolicy():
  return render_template('privacypolicy.html')

@app.route('/securefilestorage')
def securefilestorage():
  return render_template('securefilestorage.html')

@app.route('/hybridcryptography')
def hybridcryptography():
  return render_template('hybridcryptography.html')


@app.route('/service')
def service():
  return render_template('service.html')

@app.route('/why')
def why():
  return render_template('why.html')

@app.route('/login')
def login():
  return render_template('login.html')

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/return-files-key/')
def return_files_key():
  try:
    return send_file('./Original.txt', download_name='Original.txt', as_attachment=True)
  except Exception as e:
    return str(e)

@app.route('/return-files-data/')
def return_files_data():
  try:
    return send_file('./Output.txt', download_name='Output.txt', as_attachment=True)
  except Exception as e:
    return str(e)


@app.route('/data/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      return render_template('Nofile.html')
    file = request.files['file']
    if file.filename == '':
      return render_template('Nofile.html')
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'Original.txt'))
      return start()
       
    return render_template('Invalid.html')
  
  
@app.route('/')
@app.route('/login1', methods =['GET', 'POST'])
def login1():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login1.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login1'))
  
  
@app.route('/download_file')
def download_file():
    # Assuming you have a way to retrieve the original uploaded file
    # For example, you could store the file in a database or file system
    file_path = '/path/to/original/uploaded/file.txt'
    return send_file('./Output.txt', download_name='Output.txt', as_attachment=True)
  
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
  
    
if __name__ == '__main__':
  app.run(debug=FALSE)
