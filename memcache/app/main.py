
from itertools import count
from multiprocessing.sharedctypes import Value
from flask import render_template, url_for, request
from app import webapp, memcache
import pymysql
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from flask import json
from flask_mysqldb import MySQL,MySQLdb
mysql = MySQL(webapp)
db=pymysql.connect("localhost","root","","testingdb")
cursor=db.cursor()
Value="unknow"
count=0


@webapp.route('/')
def main():
    return render_template("main.html")

@webapp.route('/get',methods=['POST'])
def get():
    key = request.form.get('fname')
    cursor = mysql.connection.cursor()
    if key in memcache:
        value = memcache[key]
        response = webapp.response_class(
            response=json.dumps(value),
            status=200,
            mimetype='application/json'
        )
    else:
         sql="SELECT file_name FROM imagee WHERE fname=(%s)"
         cursor.execute(sql,key)
       
         value= cursor.fetchall()
         memcache[key]=value
         count=0
    return render_template("main2.html", res=value[0][0],c=count)
    

    

@webapp.route('/upload',methods=['POST'])
def upload():
    key = request.form.get('fname')
    file = request.files['file']
    filename = secure_filename(file.filename)
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    file.save(os.path.join("app/static/image", filename))
    memcache[key] = file
    cur.execute("INSERT INTO imagee (file_name, uploaded_on,fname) VALUES (%s, %s,%s)",[filename, now,key])
    mysql.connection.commit()
    response = webapp.response_class(
        response=json.dumps("OK add "),
        status=200,
        mimetype='application/json'
    )

    return response

