# bddisk-shell: Shell-like interface for pan.baidu.com
## Introduction
`bddisk-shell` is a shell-like interface for working with pan.baidu.com.
It is designed to run without any GUI and with all features available on the commandline only.
Currently it supports performing basic file operations and downloading personal as well as shared files.

## Requirements
`bddisk-shell` is programmed using Python 3 with minimum external dependencies.
To run `bddisk-shell`, you need:

* Python 3 with `requests`>=2.8.1
* `aria2c`, either in your `PATH` or in the `bddisk-shell` directory for download features

The program has been tested on various popular platforms, including Windows (both native and with WSL), Ubuntu Linux and macOS.

**Note:** Due to path issues, it may not work on Cygwin.

## Usage
In order to achieve full functionality on the commandline, `bddisk-shell` logs in to pan.baidu.com using cookies to avoid encountering a verification code.

Start the program with `python start.py`.

When running for the first time, you must provide two cookies, `BDUSS` and `STOKEN`, to the command prompt.
You can find these by capturing any request to pan.baidu.com in your browser's developer tools and viewing the cookies tab.
After the prompt, your cookies will be saved and you won't be asked to provide them the next time you log in.

Once you've logged in, you can use familiar commands to navigate and operate, these include:

* `ls`: The `-l` switch and sorting switches `-s`, `-t`, `-a` are supported. But please pass them separately as in `ls -l -s ../`.
* `cd`: Changes working directory. **Warning:** This doesn't make any requests and thus won't check validity. If you try to perform operations within a nonexistent directory, an exception will be raised.
* `rm`: Supports deleting multiple files provided as arguments. **Warning:** It won't report any errors if at least one deletion succeeds.
* `rename`: Renames given file. We don't support `mv` and this only supports renaming. Please provide only the file name as the second argument as in `rename /temp/file1 file2`.
* `cp`: Do not include file name in the destination. If you wish to rename the copied file, do this `cp /file1 /folder file2`.

The commands below are for downloading and require `aria2c`.

* `clientdl`: Downloads a given file using the client API. A local path may be provided for location of the download.
* `restdl`: Downloads a given file using the REST API. A local path may be provided for location of the download.

Please, don't ask me what differences they have.

The commands below are for accessing shared files.

* `getshare`: This gets a cookie for accessing a private shared repository. Pass the share URL (the whole string after `pan.baidu.com/s/`) and passcode as arguments. **Note:** Popular downloads may require a verification code to access. This is beyond the scope of a commandline script and will not be considered a bug.
* `transfer`: Transfers a shared repository to your personal storage. Currently only single file transfers have been tested. Pass the share URL and destination as arguments. **Note:** Please run `getshare` first for a private shared repository. Access to only one repository is granted each time, so you have to run `getshare` again if you'd like to transfer the same repository after accessing other repositories.

All commands accepting paths as arguments above support the use of absolute/relative path as well as `.`, `..` and `-`.
