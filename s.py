from http.server import BaseHTTPRequestHandler,HTTPServer

from requests import get, post
class mybackend(BaseHTTPRequestHandler):
    def do_GET(self):
        self.headers['host']='pops.vn'
        res=get('http://pops.vn'+self.path,headers=self.headers)
        self.send_response_only(res.status_code)
        for k,v in res.headers.items():
            self.send_header(k,v)
        self.end_headers()
        self.wfile.write(b'123123123')
        # print(res.content)
    def do_POST(self):
        self.headers['host']='pops.vn'
        res=post('http://pops.vn'+self.path,headers=self.headers)
        self.send_response(res.status_code)
        for k,v in res.headers.items():
            self.send_header(k,v)
        self.end_headers()
        self.wfile.write(res.content)
s=HTTPServer(('',80),mybackend)
print('Started server!')
s.serve_forever()