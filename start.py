#!/usr/bin/env python3
import requests
import sys
import os

cwd = os.getcwd()
os.chdir(os.path.realpath(__file__))

import bderrno
import login
import repl

print('Starting bddisk-shell...')
session = requests.Session()
session.headers['User-Agent'] = ''
try:
    bduss, stoken = login.read_cookie()
except FileNotFoundError:
    bduss, stoken = login.cookie_prompt()
    login.save_cookie(bduss, stoken)
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
try:
    repl.repl(session, username, bdstoken)
except KeyboardInterrupt:
    print("Interrupted by user, exit now.")

