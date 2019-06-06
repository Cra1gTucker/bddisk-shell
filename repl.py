import sys
import os

import bderrno
import bdfiles
import bddl


def repl(session, username, bdstoken):
    cmd = ''
    path_stack = ['/']
    while cmd != 'exit':
        print('\033[92m' + username + '@bddisk\033[0m:\033[94m' + path_stack[-1] + ' \033[0m$ ', end = '')
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
        elif arg_list[0] == 'restdl':
            arg_list.pop(0)
            handle_restdl(arg_list, path_stack, session)
        elif arg_list[0] == 'rm':
            arg_list.pop(0)
            handle_rm(arg_list, path_stack, session, bdstoken)

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
                print("\033[91mInvalid argument: '" + arg + "'\033[0m", file = sys.stderr)
                return
    except IndexError:
        # no arguments given
        pass
    realpath = pathFromArgs(arg_list, path_stack)
    try:
        bdfiles.listFiles(bdfiles.getFileJson(session, bdstoken, path = realpath, order = order, desc = desc), long_list = long_list)
    except FileNotFoundError:
        print("\033[91mFile not found: '" + realpath + "'\033[0m", file = sys.stderr)
#cd [PATH]
def handle_cd(arg_list, path_stack):
    # Warning: this function does not check whether the directory exists
    path_stack.append(pathFromArgs(arg_list, path_stack))

def handle_restdl(arg_list, path_stack, session):
    full_path = pathFromArgs(arg_list, path_stack)
    bddl.REST_download(session, bddl.REST_params(full_path))
# rm [FILE1] [FILE2] ...
# Warning: BaiduNetDisk doesn't report error when at least one action is successful
# so unless all files given are not found, no error will be reported
def handle_rm(arg_list, path_stack, session, bdstoken):
    file_list = []
    for arg in arg_list:
        file_list.append(pathFromArgs([arg], path_stack))
    try:
        bdfiles.deleteFiles(session, bdstoken, file_list)
    except FileNotFoundError:
        print('\033[91mFile(s) not found.\033[0m', file = sys.stderr)

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
