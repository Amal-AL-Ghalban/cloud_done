#app.py
from flask import Flask, render_template, flash, redirect, request,jsonify
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from memcache import memcache
import os

from datetime import datetime
memcache={}
#import magic

webapp= Flask(__name__, template_folder="template")

value={}
count=0
counthit=0
countmiss=0
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

   
@webapp.route('/')
def index():
    return render_template('index.html')
@webapp.route('/upload', methods=['POST','GET'])
def upload():
    
    
    now = datetime.now()
    file = request.files['inputFile']
    fname = request.form['fname']
    filename = secure_filename(file.filename)
    mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor = mysql.connection.cursor()
    # row = cursor.execute("SELECT fname FROM imagee").fetchone()
    cursor.execute("SELECT fname FROM imagee WHERE fname = %s",[fname])
    row = cursor.fetchone() 

         
    if file and allowed_file(file.filename):
      file.save(os.path.join(webapp.config['UPLOAD_FOLDER'], filename))
      cursor = mysql.connection.cursor()
      cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
      if not row:
           
           
        # 
           cur.execute("INSERT INTO imagee (file_name,uploaded_on,fname) VALUES (%s,%s,%s)",[filename,now,fname])
           mysql.connection.commit()
        #    count=0
        #    flash(count)
           flash('Upload sussesful',count)  
           return redirect('/')  
           
      else:
           flash('key is exist please enter another')  
           return redirect('/')
    else:
     flash('Allowed image types are -> png, jpg, jpeg, gif')  
    return redirect('/') 
           
  
@webapp.route('/search')
def search():
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
     



@webapp.route('/Display')
def Disp(): 
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM imagee")
    imageelist = cur.fetchall()
    return render_template('display.html', imageelist=imageelist)
 
@webapp.route("/fetchdata",methods=["POST","GET"])
def fetchdata():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        cur.execute("SELECT * FROM imagee WHERE fname = %s", [fname])
        rs = cur.fetchone() 
        
        file = rs['inputFile']
        print(file)
    return jsonify({'htmlRespone': render_template('Respone.html', name=fname, photo=file)})



@webapp.route('/memcache')
def memcache():
    return render_template('cache.html')
@webapp.route('/mem',methods=['post'])
def mem():
   
    
    
    key = request.form['fname']
    
   
    # row = cursor.execute("SELECT fname FROM imagee").fetchone(
    
    
   
    
    if key in memcache:
        value[0] = memcache[key]
        m=memcache.get(key)
        global counthit
        counthit=counthit+1   
        return render_template("main2.html",c=counthit)     
    else:
         cursor = mysql.connection.cursor()
         cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
         sql = "SELECT file_name from imagee WHERE fname LIKE (%s)"
         cursor.execute(sql,key)
         value= cursor.fetchall()
         memcache[key]=value[0]
        
         mysql.connection.commit()
         countmiss=countmiss+1
         return render_template("main2.html",c=countmiss)
    
if __name__ == '__main__':
    webapp.run(debug=True) 



