# download commands
import random
import json
import requests
import os
import urllib

import bderrno

def REST_params(full_path):
    return urllib.urlencode({
        'method':'download',
        'path':full_path,
        'random':random.random(),
        'app_id':'498065'
    })

def REST_download(session, paramstr, cookie_file, dest = '.'):
    os.system('aria2c -d ' + dest + ' --load-cookies ' + cookie_file + ' https://pcs.baidu.com/rest/2.0/pcs/file?' + paramstr)

def ClientAPI_dl(session, path, dest):
    pass