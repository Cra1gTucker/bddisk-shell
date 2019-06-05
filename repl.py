import json
import sys
import os

import bderrno
import bdfiles


def repl(session, username, bdstoken):
    cmd = ''
    path_stack = ['/']
    while cmd != 'exit':
        print(username + '@bddisk:' + path_stack[-1] + ' $ ', end = '')
        cmd = input()
        arg_list = cmd.split()
        if arg_list[0] == 'ls':
            arg_list.pop(0)
            try:
                if arg_list[-1][0] == '-':
                    # no path given
                    arg_list.append(path_stack[-1])
            except IndexError:
                # no path or arguments given
                arg_list.append(path_stack[-1])
            handle_ls(arg_list, path_stack, session, bdstoken)
        elif arg_list[0] == 'cd':
            arg_list.pop(0)
            handle_cd(arg_list, path_stack)
# ls -l -t -s -a [PATH]
def handle_ls(arg_list, path_stack, session, bdstoken):
    long_list = False
    order = 'name'
    desc = True
    try:
        for arg in arg_list[:-1]:
            if arg == '-l':
                long_list = True
            elif arg == '-t':
                order = 'time'
            elif arg == '-s':
                order = 'size'
            elif arg == '-a':
                desc = False
            else:
                print("Invalid argument: '" + arg + "'", file = sys.stderr)
                return
    except IndexError:
        # no arguments given
        pass
    
    try:
        if arg_list[-1][0] == '/':
            # absolute path
            bdfiles.listFiles(bdfiles.getFileJson(session, bdstoken, path = arg_list[-1], order = order, desc = desc), long_list = long_list)
        else:
            # relative path
            bdfiles.listFiles(bdfiles.getFileJson(session, bdstoken, path = path_stack[-1] + arg_list[-1], order = order, desc = desc), long_list = long_list)
    except FileNotFoundError:
        print("File not found: '" + arg_list[-1] + "'", file = sys.stderr)
#cd [PATH]
def handle_cd(arg_list, path_stack):
    # Warning: this function does not check whether the directory exists
    try:
        if arg_list[-1][0] == '/':
            path_stack.append(arg_list[-1])
        else:
            path_stack.append(path_stack[-1] + arg_list[-1])
    except IndexError:
        # no path given, do nothing
        pass
