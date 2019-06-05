# exception definitions

class bdhttp_error(Exception):
    pass
class bdlogin_error(Exception):
    pass

def bderrno(r_json):
    if r_json['errno'] == 1 or r_json['errno'] == 2:
        raise FileNotFoundError
    if r_json['errno'] == 0:
        return
    else:
        raise bdlogin_error