# download commands
import random
import requests
import os
import urllib.parse
import json
from datetime import datetime
from time import sleep

import bderrno

def REST_params(full_path):
    return urllib.parse.urlencode({
        'method':'download',
        'path':full_path,
        'random':random.random(),
        'app_id':'498065'
    })

def REST_download(session, paramstr, dest = '.'):
    # aria2 will report error, so don't raise FileNotFoundError
    cookieHeader = 'Cookie: BAIDUID=' + requests.utils.dict_from_cookiejar(session.cookies)['BAIDUID'] + '; BDUSS=' + requests.utils.dict_from_cookiejar(session.cookies)['BDUSS'] + '; cflag=13%3A3'
    os.system('aria2c -x 16 -d "' + dest + '" --header "' + cookieHeader + '" "https://pcs.baidu.com/rest/2.0/pcs/file?' + paramstr + '"')

def ClientAPI_dl(session, full_path, dest = '.'):
    query = {
        'app_id':'250528',
        'channel':'00000000000000000000000000000000',
        'check_blue':'1',
        'clienttype':'8',
        'devuid':'0',
        'dtype':'1',
        'ehps':'0',
        'err_ver':'1.0',
        'es':'1',
        'esl':'1',
        'method':'locatedownload',
        'ver':'4.0',
        'version':'6.7.4.2',
        'vip':'2',
        'time':str(int(datetime.now().timestamp())) + '000',
        'path':full_path
    }
    headers = {
        'Accept':'*/*',
        'User-Agent':'netdisk;6.7.4.2;PC;PC-Windows;10.0.17763;WindowsBaiduYunGuanJia',
        'Content-Type':'application/x-www-form-urlencoded'
    }
    r = session.post('https://d.pcs.baidu.com/rest/2.0/pcs/file', params = query, data = b' ', headers = headers)
    if r.status_code >= 400:
        raise bderrno.bdhttp_error
    url_list = json.loads(r.content)['urls']
    urls_str = ''
    for url_dict in url_list:
        urls_str += ('"' + url_dict['url'] + '" ')
    print('\033[92mWaiting 5 seconds to allow server preparation.\033[0m')
    sleep(5)
    os.system('aria2c -x 16 -d "' + dest + '" -U "netdisk;6.7.4.2;PC;PC-Windows;10.0.17763;WindowsBaiduYunGuanJia" ' + urls_str)
