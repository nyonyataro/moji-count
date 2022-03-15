from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os, re
import numpy as np
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://lrhhnqhwdpefuq:b449ee67154367aad5e307990cd777aa6e0f31e178f73b0b7a12034ad38125d9@ec2-3-216-221-31.compute-1.amazonaws.com:5432/d9uorpc13ahg44"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)

def write(score):
    data = Scores(score = score)
    db.session.add(data)
    db.session.commit()

def get_deviation(score):
    scores = Scores.query.all()
    nums = []
    for row in scores:
        nums.append(int(row.score))
    list_sum = sum(nums)
    avr = list_sum/(len(nums))
    st_devidation = np.std(nums)
    devidation = (score - avr)/st_devidation * 10 + 50
    devidation = round(devidation, 1)
    return devidation


def delete(data):
    # data = txt
    #一行目削除
    data = re.sub('\[LINE].+履歴', '', data)
    #二行目削除
    data = re.sub('保存日時：20[0-9]{2}/[0-9]+/[0-9]+ [0-9]+:[0-9]{1,2}', '', data)
    #日付削除
    data = re.sub('20[0-9]{2}/[0-9]+/[0-9]+\(.\)', '', data)
    #メッセージの前の時間と名前削除
    data = re.sub('[0-9]+:[0-9]+\s\S+\s', '', data)
    #改行・スペース削除
    data = re.sub('\n', '', data)
    data = re.sub('\s', '', data)
    return data

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
            filepath = 'tmp/' + secure_filename(f.filename)
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