from http.server import BaseHTTPRequestHandler,HTTPServer

from requests import get, post
class mybackend(BaseHTTPRequestHandler):
    def do_GET(self):
        myheader=self.headers
        myheader['host']='pops.vn'
        res=get('http://pops.vn'+self.path,headers=myheader)
        self.send_response(res.status_code)
        # for k,v in res.headers.items():
        #     self.send_header(k,v)
        self.send_header('content-type',res.headers['content-type'])
        self.send_header('set-cookie',res.headers['set-cookie'])
        self.end_headers()
        self.wfile.write(res.content.replace(b'https://cdn.popsww.com',b'http://localhost:8080').replace(b'https://stream.popsww.com',b'http://localhost:8081'))
        # print(res.content)
    def do_POST(self):
        self.headers['host']='pops.vn'
        res=post('http://pops.vn'+self.path,headers=self.headers)
        self.send_response(res.status_code)
        # for k,v in res.headers.items():
        #     self.send_header(k,v)
        self.send_header('content-type',res.headers['content-type'])
        self.send_header('set-cookie',res.headers['set-cookie'])
        self.end_headers()
        self.wfile.write(res.content)
s=HTTPServer(('',80),mybackend)
print('Started server!')
s.serve_forever()