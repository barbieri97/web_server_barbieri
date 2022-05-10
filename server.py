from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
from urllib.parse import parse_qs
from parse import parse
from json import dumps

import cgi


class _handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        #host, port = self.client_address
        self._set_headers()
        f = open('index.html', 'rb')
        self.wfile.write(f.read())
        f.close()

    def do_POST(self):
        ctype, _ = cgi.parse_header(self.headers['content-type'])
        # pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        if ctype == 'multipart/form-data':
            # fields = cgi.parse_multipart(self.rfile, pdict)
            # content = fields.get('myfile')
            lenght = self.headers.get('content-length')
            request = self.rfile.read(int(lenght))
            dic, content = parse(request)
            f = open(f"files/{dic['filename']}", 'wb')
            f.write(content)
            f.close()
            self._set_headers()
            f = open('post_realizado.html', 'rb')
            self.wfile.write(f.read())
            f.close() 
        if ctype == 'application/x-www-form-urlencoded':
            lenght = self.headers.get('content-length')
            request = self.rfile.read(int(lenght))
            data = parse_qs(request.decode('utf-8'))
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(dumps(data).encode())
            print(data)
            

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, _handler)
    print(f'servido no porta {server_address[1]}')
    httpd.serve_forever()
