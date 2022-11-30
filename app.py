#app.py
from flask import Flask, render_template, flash, redirect, url_for, request,jsonify
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import pymysql
from datetime import datetime
from memcache import memcache
#import magic
import urllib.request
webapp = Flask(__name__, template_folder="template")
 
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#                                                       #password:admin
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:admin@localhost/sampledb'
  
# db=SQLAlchemy(app)
 
webapp.config['SECRET_KEY'] = 'cairocoders-ednalan'
webapp.config['MYSQL_HOST'] = 'localhost'
webapp.config['MYSQL_USER'] = 'root'
webapp.config['MYSQL_PASSWORD'] = ''
webapp.config['MYSQL_DB'] = 'testingdb'
webapp.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(webapp)
  
UPLOAD_FOLDER = 'static/uploads'
webapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
   
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
   
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
# class Student(db.Model):
#   __tablename__='students'
#   id=db.Column(db.Integer,primary_key=True)
#   fname=db.Column(db.String(40))
  
#   email=db.Column(db.String(40))
#   profile_pic = db.Column(db.String(150))
 
  def __init__(self,fname,email,profile_pic):
    self.fname=fname
    self.email=email
    self.profile_pic=profile_pic
   
@webapp.route('/')
def index():
    return render_template('index.html')
  
@webapp.route('/upload', methods=['POST','GET'])
def upload():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    file = request.files['inputFile']
    fname = request.form['fname']
    filename = secure_filename(file.filename)
    
    if file and allowed_file(file.filename):
       file.save(os.path.join(webapp.config['UPLOAD_FOLDER'], filename))
       cur.execute("INSERT INTO imagee (file_name, uploaded_on,fname) VALUES (%s, %s,%s)",[filename, now,fname])
       mysql.connection.commit()
       print(file)
       flash('File successfully uploaded ' + file.filename + ' to the database!')
       return redirect('/')
    else:
        flash('Invalid Uplaod only  png, jpg, jpeg, gif') 
    return redirect('/') 

@webapp.route('/search')
def ser():
    return render_template('ser.html')    
@webapp.route("/ajaxlivesearch",methods=["POST","GET"])
def ajaxlivesearch():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        search_word = request.form['query']
        print(search_word)
        if search_word == '':
            query = "SELECT * from imagee"
            cur.execute(query)
            imagee = cur.fetchall()
        else:    
            query = "SELECT * from imagee WHERE fname LIKE '%{}%'".format(search_word)
            cur.execute(query)
            numrows = cur.rowcount
            imagee = cur.fetchall()
            
    return jsonify({'htmlresponse': render_template('response.html',imagee=imagee,numrows=numrows)})
     
@webapp.route('/memcache')
def memcache():
    return render_template('cache.html')
@webapp.route('/mem',methods=['post'])
def mem():
   key=request.form['fname']
   if key in memcache:
      value[0]=memcache[key]
      n=memcache.get(key)
      global counthit
      counthit=counthit+1
      print (counthit,"pp")
      print(memcache)
      count=1
      return render_template("main2.html",c=count,counthit=counthit)
   else:
      conn=pymysql.connect(host='localhost',user='root',password='',db='testingdb')
      cur=conn.cursor()
      sql="SELECT file_name from imagee where fname=%s"
      cur.execute(sql,key)
      value=cur.fetchall()
      memcache[key]=value[0]
      count=0
      global countmiss
      countmiss=countmiss+1
      flash (countmiss,"pp")
      print(memcache)
      return render_template("main2.html",c=count,countmiss=countmiss)

@webapp.route('/display')
def display():
    imageList = os.listdir('static/uploads')
    imagelist = ['uploads/' + image for image in imageList]
    return render_template("display.html", imagelist=imagelist)
 

      
if __name__ == '__main__':
    webapp.run(debug=True) 



