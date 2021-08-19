# Contains commands to perform file actions
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
        raise bderrno.bdhttp_error
    r_json = json.loads(response.content)
    bderrno.bderrno(r_json)
    return r_json['list']

# server_mtime is date in unix timestamp
def listFiles(list_json, long_list = False):
    if long_list:
        for file in list_json:
            print('%24s\t%s\t%s' % (file['server_filename'], datetime.fromtimestamp(file['server_mtime']).strftime('%Y-%m-%d %H:%M:%S'), str(file['size'])))
    else:
        for file in list_json:
            print('%s' % file['server_filename'])

def deleteFiles(session, bdstoken, file_list):
    dataStr = 'filelist=["' + file_list[0] + '"'
    for items in file_list[1:]:
        dataStr += (',"' + items + '"')
    dataStr += ']'
    r_json = json.loads(session.post('https://pan.baidu.com/api/filemanager?opera=delete&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528&bdstoken=' + bdstoken + '&clienttype=0', headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}, data = bytes(dataStr, 'utf-8')).content)
    bderrno.bderrno(r_json)

def renameFile(session, bdstoken, full_path, newname):
    dataStr = 'filelist=[{"path":"' + full_path + '","newname":"' + newname + '"}]'
    r_json = json.loads(session.post('https://pan.baidu.com/api/filemanager?opera=rename&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528&bdstoken=' + bdstoken + '&clienttype=0', headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}, data = bytes(dataStr, 'utf-8')).content)
    bderrno.bderrno(r_json)

def copyFile(session, bdstoken, full_path, dest, newname):
    dataStr = 'filelist=[{"path":"' + full_path + '","dest":"' + dest + '","newname":"' + newname + '"}]'
    r_json = json.loads(session.post('https://pan.baidu.com/api/filemanager?opera=copy&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528&bdstoken=' + bdstoken + '&clienttype=0', headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}, data = bytes(dataStr, 'utf-8')).content)
    bderrno.bderrno(r_json)

def newFolder(session, bdstoken, full_path):
    dataStr = 'path=' + full_path + '&isdir=1&block_list=[]'
    r_json = json.loads(session.post('https://pan.baidu.com/api/create?a=commit&channel=chunlei&web=1&app_id=250528&bdstoken=' + bdstoken + '&clienttype=0', headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}, data = bytes(dataStr, 'utf-8')).content)
    bderrno.bderrno(r_json)
