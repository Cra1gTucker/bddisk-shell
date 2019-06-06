# exception definitions

class bdhttp_error(Exception):
    pass
class bdlogin_error(Exception):
    pass

def bderrno(r_json):
    if r_json['errno'] == 0:
        return
    if r_json['errno'] == 1 or r_json['errno'] == 2 or r_json['errno'] == -9:
        raise FileNotFoundError
    else:
        raise bdlogin_error