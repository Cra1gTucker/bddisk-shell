from bderrno import bderrno

import json


def verifyShare(session, bdstoken, surl, pwd):
    dataStr = 'pwd=' + pwd + '&code=&vcodestr='
    # here we'll gain a BDCLND cookie for accessing private shared file
    r_json = json.loads(session.post('https://pan.baidu.com/share/verify?surl=' + surl + '&channel=chunlei&web=1&app_id=250528&bdstoken=' + bdstoken + '&clienttype=0', headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8", "Referer":"https://pan.baidu.com/"}, data = bytes(dataStr, 'utf-8')).content)
    bderrno(r_json)