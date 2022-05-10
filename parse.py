def parse(multipart: bytes):

    head_multipart, body = multipart.split(b'\r\n\r\n')

    head_multipart = head_multipart.replace(b'=', b': ').replace(b'"', b'').replace(b'\r\n', b';')
    hbytes = head_multipart.split(b';')
    hstr = []
    for item in hbytes:
        hstr.append(item.decode('utf-8').strip())
    boundary = hstr.pop(0)
    dic = {}
    for item in hstr:
        k, v = item.split(': ')
        dic[k] = v

    body = body.replace(boundary.encode() + b'--', b'')
    return dic, body



