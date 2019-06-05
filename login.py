# Contains code to login to BaiduNetDisk
# We need two cookies to login, they are BDUSS and STOKEN

import requests
import re

import bderrno
def cookie_prompt():
    print("Enter BDUSS value:")
    bduss = input()
    print("Enter STOKEN value:")
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
    if r.status_code > 400:
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