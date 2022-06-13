from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from mimetypes import guess_type
remixing={
    'popsapp/assets/js/videojs-youtube.min.js':'a.js'
}

from requests import get, post
class mybackend(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path[1:] in remixing:
            self.send_response(200)
            self.send_header('content-type',guess_type(remixing[self.path[1:]])[0])
            self.end_headers()
            self.wfile.write(open(remixing[self.path[1:]],'rb').read())
        else:
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