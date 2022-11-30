
from flask import Flask,render_template, url_for, request
from app import webapp,memcache
from flask import json

import pymysql
from werkzeug.utils import secure_filename
app = Flask(__name__)
db=pymysql.connect("localhost","root","","testingdb")
cursor=db.cursor()
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
value ="unknow"
count=0
@webapp.route('/')
def main():
    return render_template("index.html")

@webapp.route('/upload', methods=['POST','GET'])
def upload():
    key = request.form.get('fname')

    if key in memcache:
        value = memcache[key]
        count=1
    else:
        sql = "SELECT file_name from imagee WHERE fname LIKE (%s)"
        cursor.execute(sql.key)
        value= cursor.fetchall()
        memcache[key]=value
        count=0
    return render_template("index.html", res=value[0][0],c=count)
    




