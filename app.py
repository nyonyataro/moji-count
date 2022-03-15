import re

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