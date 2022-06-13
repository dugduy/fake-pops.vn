from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer

from requests import get, post
class mybackend(BaseHTTPRequestHandler):
    def do_GET(self):
        myheader=self.headers
        myheader['host']='cdn.popsww.com'
        res=get('https://cdn.popsww.com'+self.path,headers=myheader)
        self.send_response(res.status_code)
        # for k,v in res.headers.items():
        #     self.send_header(k,v)
        self.send_header('content-type',res.headers['content-type'])
        # self.send_header('set-cookie',res.headers['set-cookie'])
        self.end_headers()
        self.wfile.write(res.content)
        # print(res.content)
    def do_POST(self):
        self.headers['host']='cdn.popsww.com'
        res=post('https://cdn.popsww.com'+self.path,headers=self.headers)
        self.send_response(res.status_code)
        # for k,v in res.headers.items():
        #     self.send_header(k,v)
        self.send_header('content-type',res.headers['content-type'])
        self.send_header('set-cookie',res.headers['set-cookie'])
        self.end_headers()
        self.wfile.write(res.content)
s=ThreadingHTTPServer(('',8080),mybackend)
print('Started server!')
s.serve_forever()