# Contains code to login to BaiduNetDisk
# We need two cookies to login, they are BDUSS and STOKEN

def cookie_prompt():
    print("Enter BDUSS value:")
    bduss = input()
    print("Enter STOKEN value:")
    stoken = input()
    return bduss, stoken

def gen_cookie(bduss, stoken):
    bduss_cookie = {
        "name":'BDUSS',
        "value":bduss
    }
    stoken_cookie = {
        "name":'STOKEN',
        "value":stoken
    }
    return bduss_cookie, stoken_cookie

def login(session, bduss_cookie, stoken_cookie):
    session.cookies.set(**bduss_cookie)
    session.cookies.set(**stoken_cookie)
    code = session.get('https://pan.baidu.com/', headers = {"User-Agent":""}).status_code
    #set User-Agent to '' because requests UA is banned
    if code > 400:
        raise http_error
    return code