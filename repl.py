import sys
import os
import pathlib

import bderrno
import bdfiles
import bddl

def repl(session, username, bdstoken):
    cwd = pathlib.PurePath(os.getcwd())
    print('\033[92mChecking aria2c...\033[0m')
    aria2_path = 'aria2c'
    if os.system('which aria2c') and os.system('where aria2c'):
        aria2_path = str(pathlib.PurePath(pathlib.PurePath(os.path.realpath(__file__)).parent, 'aria2c'))
    os.chdir(pathlib.PurePath(os.path.realpath(__file__)).parent)
    cmd = ''
    path_stack = ['/']
    while cmd != 'exit':
        print('\033[92m' + username + '@bddisk\033[0m:\033[94m' + path_stack[-1] + ' \033[0m$ ', end = '')
        cmd = input()
        arg_list = trimArgs(cmd)
        if len(arg_list) == 0:
            print()
            continue
        verb = arg_list.pop(0)
        if verb == 'ls':
            try:
                if arg_list[-1][0] == '-':
                    # no path given
                    arg_list.append(path_stack[-1])
            except IndexError:
                # no path or arguments given
                arg_list.append(path_stack[-1])
            handle_ls(arg_list, path_stack, session, bdstoken)
        elif verb == 'cd':
            handle_cd(arg_list, path_stack)
        elif verb == 'clientdl':
            handle_clientdl(arg_list, path_stack, session, cwd, aria2_path)
        elif verb == 'restdl':
            handle_restdl(arg_list, path_stack, session, cwd, aria2_path)
        elif verb == 'rm':
            handle_rm(arg_list, path_stack, session, bdstoken)
        elif verb == 'rename':
            handle_rename(arg_list, path_stack, session, bdstoken)
        elif verb == 'cp':
            handle_cp(arg_list, path_stack, session, bdstoken)


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
# cd [PATH]
def handle_cd(arg_list, path_stack):
    # Warning: this function does not check whether the directory exists
    path_stack.append(pathFromArgs(arg_list, path_stack))
# restdl [LOCATION] [FILE]
def handle_restdl(arg_list, path_stack, session, cwd, aria2_path):
    full_path = pathFromArgs(arg_list, path_stack)
    os.chdir(cwd)
    loc = ''
    try:
        loc = arg_list[-2]
    except IndexError:
        loc = str(cwd)
    bddl.REST_download(session, bddl.REST_params(full_path), aria2_path, dest = loc)
    os.chdir(os.path.dirname(pathlib.PurePath(os.path.realpath(__file__))))
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
# clientdl [LOCATION] [FILE]
def handle_clientdl(arg_list, path_stack, session, cwd, aria2_path):
    os.chdir(cwd)
    full_path = pathFromArgs(arg_list, path_stack)
    loc = ''
    try:
        loc = arg_list[-2]
    except IndexError:
        loc = str(cwd)
    bddl.ClientAPI_dl(session, full_path, aria2_path, dest = loc)
    os.chdir(os.path.dirname(pathlib.PurePath(os.path.realpath(__file__))))
# rename [FILE] [NEWNAME]
def handle_rename(arg_list, path_stack, session, bdstoken):
    if len(arg_list) == 2:
        full_path = pathFromArgs(arg_list[:1], path_stack)
        try:
            bdfiles.renameFile(session, bdstoken, full_path, arg_list[1])
        except FileNotFoundError:
            print("\033[91mFile not found: '" + full_path + "'\033[0m", file = sys.stderr)
    else:
        print('\033[93mUsage: rename [FILE] [NEWNAME]\033[0m', file = sys.stderr)
# cp [FILE] [DEST] [NEWNAME]
def handle_cp(arg_list, path_stack, session, bdstoken):
    if len(arg_list) == 2:
        dest = pathFromArgs(arg_list, path_stack)
        full_path = pathFromArgs(arg_list[:-1], path_stack)
        try:
            bdfiles.copyFile(session, bdstoken, full_path, dest, os.path.basename(full_path))
        except FileNotFoundError:
            print('\033[91mFile(s) not found.\033[0m', file = sys.stderr)
    elif len(arg_list) == 3:
        newname = arg_list[-1]
        dest = pathFromArgs(arg_list[:-1], path_stack)
        full_path = pathFromArgs(arg_list[:-2], path_stack)
        try:
            bdfiles.copyFile(session, bdstoken, full_path, dest, newname)
        except FileNotFoundError:
            print('\033[91mFile(s) not found.\033[0m', file = sys.stderr)
    else:
        print('\033[93mUsage: cp [FILE] [DEST] [NEWNAME]\033[0m', file = sys.stderr)

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
            return ('/' + arg_list[-1]) if path_stack[-1] == '/' else (path_stack[-1] + '/' + arg_list[-1])
    except IndexError:
        # no path or arguments given
        return path_stack[-1]

def trimArgs(cmd):
    arg_list = []
    inQuote = False
    arg = ''
    for char in cmd:
        if char == ' ':
            if not inQuote:
                if arg != '':
                    arg_list.append(arg)
                    arg = ''
            else:
                arg += char
        elif char == '"':
            inQuote = not inQuote
            if not inQuote:
                if arg != '':
                    arg_list.append(arg)
                    arg = ''
        else:
            arg += char
    if arg != '':
        arg_list.append(arg)
    return arg_list
        