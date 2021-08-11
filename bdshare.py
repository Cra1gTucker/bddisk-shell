from bderrno import bderrno

import json
import re
from requests.utils import dict_from_cookiejar
from urllib.parse import quote, unquote

def verifyShare(session, bdstoken, surl, pwd):
    dataStr = 'pwd=' + pwd + '&code=&vcodestr='
    # here we'll gain a BDCLND cookie for accessing private shared file
    r_json = json.loads(session.post('https://pan.baidu.com/share/verify?surl=' + surl + '&channel=chunlei&web=1&app_id=250528&bdstoken=' + bdstoken + '&clienttype=0', headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8", "Referer":"https://pan.baidu.com/"}, data = bytes(dataStr, 'utf-8')).content)
    bderrno(r_json)

def transferShare(session, bdstoken, surl, dest):
    response = session.get('https://pan.baidu.com/s/' + surl, allow_redirects=False)
    if response.status_code >= 400:
        raise FileNotFoundError
    if response.status_code >= 300:
        raise PermissionError
    share_uk_match = re.compile('"share_uk":"([^"]+)"').search(str(response.content))
    if share_uk_match:
        share_uk = share_uk_match.group(1)
    else:
        raise PermissionError
    shareid_match = re.compile('"shareid":([^,]+)').search(str(response.content))
    if shareid_match:
        shareid = shareid_match.group(1)
    else:
        raise PermissionError
    fs_id_match = re.compile('"fs_id":([^,]+)').search(str(response.content))
    if fs_id_match:
        fs_id = fs_id_match.group(1)
    else:
        raise PermissionError
    sekey = dict_from_cookiejar(session.cookies)['BDCLND']
    params = {
        "shareid":shareid,
        "from":share_uk,
        "sekey":unquote(sekey),
        "channel":"chunlei",
        "web":"1",
        "app_id":"250528",
        "bdstoken":bdstoken,
        "clienttype":"0"
    }
    dataStr = 'fsidlist=%5B' + fs_id + '%5D&path=' + quote(dest, safe='')
    r_json = json.loads(session.post('https://pan.baidu.com/share/transfer', headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8", "Referer":"https://pan.baidu.com/"}, params = params, data = bytes(dataStr, 'utf-8')).content)
    bderrno(r_json)
