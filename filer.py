import pandas as pd
import database as db
import sys
import time
import json
import downloadjson


def getmailserver():
    with open('server.srv') as f:
        return f.read()


def contenuto(filename):
    if not filename:
        return ''
    with open(filename) as f:
        content = f.read()
    return content


def _textfile(listname):
    with open(listname) as f:
        tmp = f.read()
        tmp = tmp.replace(" ", "")
        lista = tmp.split("\n")
    return lista


def _excelfile(filename):
    data = pd.read_excel(filename, header=None)
    indirizzi = data.loc[:, 0].tolist()
    return indirizzi


def _jsonquery(dict_list, tag):
    for dictionary in dict_list:
        if tag in dictionary:
            yield dictionary[tag]


def jsonlist(data):
    tmp = []

    for tag in downloadjson.taglist:
        try:
            print('querying with keyword :', tag)
            tmp += list(_jsonquery(data, tag))
        except Exception as ex:
            print('Exception :', ex)

    if not tmp:
        return None
    return tmp


def _jsonfile(filename):
    with open(filename) as f:
        data = json.load(f)
        return jsonlist(data)


def _extract(filename):
    if filename.endswith(".txt"):
        return _textfile(filename)
    elif filename.endswith(".xls"):
        return _excelfile(filename)
    elif filename.endswith('.json'):
        return _jsonfile(filename)
    else:
        print('Format not supported')
        return None


def aggiungiscritti(filename):
    print("adding subscribers...")
    start_time = time.time()
    tmp = _extract(filename)
    if tmp is None:
        print('No subs added')
    else:
        db.addiscritti(tmp)
        print("subscribers added!")
    print('Done!------------- Time elapsed : ', round(time.time() - start_time, 6), '\n')
    return
