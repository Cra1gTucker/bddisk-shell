# Contains commands to perform file actions

import json
from datetime import datetime

import bderrno
def getFileJson(session, bdstoken, path = '/', page = '1', order = 'time', desc = '1'):
    params = {
        "order":order,
        "desc":desc,
        "showempty":"0",
        "page":page,
        "num":"100",
        "dir":path,
        "channel":"chunlei",
        "web":"1",
        "app_id":"250528",
        "bdstoken":bdstoken,
        "clienttype":"0"
    }
    response = session.get('https://pan.baidu.com/api/list',params = params)
    if response.status_code > 400:
        raise bderrno.http_error
    r_json = json.loads(response.content)
    bderrno.bderrno(r_json)
    return r_json['list']

# server_mtime is date in unix timestamp
def listFiles(list_json):
    for i in range(len(list_json)):
        print('%8s\t%s\t%s' % (list_json[i]['server_filename'], datetime.fromtimestamp(list_json[i]['server_mtime']).strftime('%Y-%m-%d %H:%M:%S'), str(list_json[i]['size'])))

