from flask import Flask, render_template, request, flash, redirect
from app import delete
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024

@app.route("/", methods = ['POST','GET'])
def hello_world():
    if request.method == 'GET':
        return render_template('index.html', post = False)
    elif request.method =='POST':
        if request.form.get('txt'):
            txt = request.form.get('txt')
        if request.files.get('file'):
            f = request.files.get('file')
            filepath = 'txt/' + secure_filename(f.filename)
            f.save(filepath)
            
            f_2 = open(filepath,'r', encoding='UTF-8')
            txt = f_2.read()
            f_2.close()
            os.remove(filepath)
        txt = delete(txt)
        return render_template('index.html',length=len(txt), post = True)