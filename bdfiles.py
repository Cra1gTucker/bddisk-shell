# Contains commands to perform file actions
import requests
import json
from datetime import datetime

import bderrno
def getFileJson(session, bdstoken, path = '/', page = '1', order = 'name', desc = True):
    params = {
        "order":order,
        "desc":'1' if desc else '0',
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
def listFiles(list_json, long_list = False):
    if long_list:
        for file in list_json:
            print('%8s\t%s\t%s' % (file['server_filename'], datetime.fromtimestamp(file['server_mtime']).strftime('%Y-%m-%d %H:%M:%S'), str(file['size'])))
    else:
        for file in list_json:
            print('%8s' % file['server_filename'])
        print()
