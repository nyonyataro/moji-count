from os import read
import re, csv
import numpy as np

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

def write(length):
    with open('scores.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([length])

def get_deviation(score):
    with open('scores.csv') as f:
        reader = csv.reader(f)
        nums = []
        for row in reader:
            nums.append(int(row[0]))
    list_sum = sum(nums)
    avr = list_sum/(len(nums))
    st_devidation = np.std(nums)
    devidation = (score - avr)/st_devidation * 10 + 50
    devidation = round(devidation,1)
    return devidation