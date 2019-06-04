# Contains commands to perform file actions

def getFileJson(session, path = '/', page = '1', order = 'time', desc = '1'):
    params = {
        "order":order,
        "desc":desc,
        "showempty":"0",
        "web":"1",
        "page":page,
        "num":"100",
        "dir":path,
        "channel":"chunlei",
        "app_id":"250528",
        "clienttype":"0"
    }
    response = session.get('https://pan.baidu.com/api/list',headers = {'User-Agent':''},params = params)
    if response.status_code > 400:
        raise http_error
    return json.loads(response.content)['list']