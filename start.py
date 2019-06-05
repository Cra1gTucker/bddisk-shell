#!/usr/bin/env python3
import requests
import json
import re
import sys

import bderrno
import login
import bdfiles

print('Starting bddisk-shell...')
session = requests.Session()
session.headers['User-Agent'] = ''
bduss, stoken = login.cookie_prompt()
bduss_cookie, stoken_cookie = login.gen_cookie(bduss, stoken)
try:
    username, bdstoken = login.login(session, bduss_cookie, stoken_cookie)
except bderrno.bdhttp_error:
    print("Couldn't connect to BaiduNetDisk!", file = sys.stderr)
    exit(1)
except bderrno.bdlogin_error:
    print("Login incorrect.", file = sys.stderr)
    exit(2)

print("Welcome to bddisk-shell, " + username + " !")