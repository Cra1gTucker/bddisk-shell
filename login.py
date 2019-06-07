# Contains code to login to BaiduNetDisk
# We need two cookies to login, they are BDUSS and STOKEN

import requests
import re

import bderrno
def cookie_prompt():
    print("Enter BDUSS value:", end = '')
    bduss = input()
    print("Enter STOKEN value:", end = '')
    stoken = input()
    return bduss, stoken

def gen_cookie(bduss, stoken):
    bduss_cookie = {
        "name":'BDUSS',
        "value":bduss
    }
    stoken_cookie = {
        "name":'STOKEN',
        "value":stoken
    }
    return bduss_cookie, stoken_cookie

def login(session, bduss_cookie, stoken_cookie):
    session.cookies.set(**bduss_cookie)
    session.cookies.set(**stoken_cookie)
    print('Logging in...')
    r = session.get('https://pan.baidu.com/')
    # when calling, set User-Agent to '' because requests UA is banned
    if r.status_code >= 400:
        raise bderrno.bdhttp_error
    bds_re = re.compile('"bdstoken"\s*:\s*"([^"]+)"', re.IGNORECASE)
    bds_match = bds_re.search(str(r.content))
    if bds_match:
        bdstoken = bds_match.group(1)
    else:
        raise bderrno.bdlogin_error
    user_re = re.compile('"username":"([^"]+)"')
    user_match = user_re.search(str(r.content))
    username = user_match.group(1)
    return username, bdstoken

def save_cookie(bduss, stoken, file = 'cookies.txt'):
    with open(file, 'w') as cookie_file:
        print('pcs.baidu.com\tTRUE\t/\tFALSE\t2147483648\tBDUSS\t' + bduss, file = cookie_file)
        print('pcs.baidu.com\tTRUE\t/\tFALSE\t2147483648\tSTOKEN\t' + stoken, file = cookie_file)
        
def read_cookie(file = 'cookies.txt'):
    # will raise FileNotFoundError
    bduss = ''
    stoken = ''
    with open(file, 'r') as cookie_file:
        content = cookie_file.read()
        bduss_re = re.compile('BDUSS\t([^\n]+)')
        bduss_match = bduss_re.search(content)
        if bduss_match:
            bduss = bduss_match.group(1)
        else:
            raise FileNotFoundError
        stoken_re = re.compile('STOKEN\t([^\n]+)')
        stoken_match = stoken_re.search(content)
        if stoken_match:
            stoken = stoken_match.group(1)
        else:
            raise FileNotFoundError
    return bduss, stoken