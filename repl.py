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
    realpath = pathFromArgs(arg_list, path_stack)
    try:
        bdfiles.listFiles(bdfiles.getFileJson(session, bdstoken, path = realpath, order = order, desc = desc), long_list = long_list)
    except FileNotFoundError:
        print("File not found: '" + realpath + "'", file = sys.stderr)
    except bderrno.bdlogin_error:
        print("Login state error!", file = sys.stderr)
#cd [PATH]
def handle_cd(arg_list, path_stack):
    # Warning: this function does not check whether the directory exists
    path_stack.append(pathFromArgs(arg_list, path_stack))

def pathFromArgs(arg_list, path_stack):
    try:
        if arg_list[-1][0] == '/':
            # absolute path
            return arg_list[-1]
        elif arg_list[-1][:2] == '..':
            # ../
            return os.path.dirname(path_stack[-1]) if len(arg_list[-1]) == 2 else os.path.dirname(path_stack[-1]) + arg_list[-1][3:]
        elif arg_list[-1][0] == '-':
            # no path given
            return path_stack[-1]
        else:
            # relative path
            return path_stack[-1] + arg_list[-1]
    except IndexError:
        # no path or arguments given
        return path_stack[-1]
