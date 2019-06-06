#!/usr/bin/env python3
import requests
import sys
import os
#TODO check/fix behavior of following 2 lines on: 
# 1. Cygwin Python running on Windows console
# 2. pure Windows Python
cwd = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

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
    print("\033[91mCouldn't connect to BaiduNetDisk!\033[0m", file = sys.stderr)
    exit(1)
except bderrno.bdlogin_error:
    print("\033[91mLogin incorrect.\033[0m", file = sys.stderr)
    exit(2)
print('\033[1m\033[93m', end = '')
print('''
 __              __        __  __            __       
/  |            /  |      /  |/  |          /  |      
$$ |____    ____$$ |  ____$$ |$$/   _______ $$ |   __ 
$$      \  /    $$ | /    $$ |/  | /       |$$ |  /  |
$$$$$$$  |/$$$$$$$ |/$$$$$$$ |$$ |/$$$$$$$/ $$ |_/$$/ 
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$      \ $$   $$<  
$$ |__$$ |$$ \__$$ |$$ \__$$ |$$ | $$$$$$  |$$$$$$  \ 
$$    $$/ $$    $$ |$$    $$ |$$ |/     $$/ $$ | $$  |
$$$$$$$/   $$$$$$$/  $$$$$$$/ $$/ $$$$$$$/  $$/   $$/ 
                                                      
\033[0m
'''
)
print("Welcome to bddisk-shell, \033[4m" + username + "\033[0m !")
try:
    repl.repl(session, username, bdstoken)
except bderrno.bdlogin_error:
    print("\033[91mLogin state error! Exit now.\033[0m")
    exit(3)
except KeyboardInterrupt:
    print("Interrupted by user, exit now.")

