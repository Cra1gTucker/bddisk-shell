#!/usr/bin/env python3
import requests
import sys
import os
import pathlib
#from colorama import init
#init()
# known issues:
# Cygwin Python running on Windows console: fails

import bderrno
import login
import repl

print('Starting bddisk-shell...')
session = requests.Session()
session.headers['User-Agent'] = ''
try:
    bduss, stoken = login.read_cookie(file = pathlib.PurePath(pathlib.PurePath(os.path.realpath(__file__)).parent, 'cookies.txt'))
except FileNotFoundError:
    bduss, stoken = login.cookie_prompt()
    login.save_cookie(bduss, stoken, file = pathlib.PurePath(pathlib.PurePath(os.path.realpath(__file__)).parent, 'cookies.txt'))
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
print(r'''
 __              __        __  __            __       
/  |            /  |      /  |/  |          /  |      
$$ |____    ____$$ |  ____$$ |$$/   _______ $$ |   __ 
$$      \  /    $$ | /    $$ |/  | /       |$$ |  /  |
$$$$$$$  |/$$$$$$$ |/$$$$$$$ |$$ |/$$$$$$$/ $$ |_/$$/ 
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$      \ $$   $$<  
$$ |__$$ |$$ \__$$ |$$ \__$$ |$$ | $$$$$$  |$$$$$$  \ 
$$    $$/ $$    $$ |$$    $$ |$$ |/     $$/ $$ | $$  |
$$$$$$$/   $$$$$$$/  $$$$$$$/ $$/ $$$$$$$/  $$/   $$/ 
                                                      
'''
)
print('\033[0m', end = '')
print("Welcome to bddisk-shell, \033[4m" + username + "\033[0m !")
try:
    repl.repl(session, username, bdstoken)
except bderrno.bdlogin_error:
    print("\033[91mLogin state error! Exit now.\033[0m")
    exit(3)
except KeyboardInterrupt:
    print("Interrupted by user, exit now.")

