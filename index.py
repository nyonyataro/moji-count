from flask import Flask, render_template, request, flash, redirect
from defs import delete, write, get_deviation
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
        #フォームに入力された時
        if request.form.get('txt'):
            txt = request.form.get('txt')
        #ファイルをアップロードされた時
        elif request.files.get('file'):
            f = request.files.get('file')
            filepath = '/tmp/' + secure_filename(f.filename)
            f.save(filepath)
            
            f_2 = open(filepath,'r', encoding='UTF-8')
            txt = f_2.read()
            f_2.close()
            os.remove(filepath)
        else:
            return redirect('/')
        txt = delete(txt)
        length = len(txt)
        write(length)
        devidation = get_deviation(length)
        return render_template('index.html',length=length, devidation = devidation, post = True)