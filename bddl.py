# download commands
import random
import requests
import os
import urllib.parse

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

def ClientAPI_dl(session, path, dest):
    pass