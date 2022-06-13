from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from mimetypes import guess_type
remixing={
    'popsapp/assets/js/videojs-youtube.min.js':'a.js',
    'v1/drm/keys?type=widevine':'a.txt'
}

from requests import get, options, post
class mybackend(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path[1:] in remixing:
            self.send_response(200)
            self.send_header('content-type',guess_type(remixing[self.path[1:]])[0])
            self.end_headers()
            self.wfile.write(open(remixing[self.path[1:]],'rb').read())
        else:
            myheader=self.headers
            myheader['host']='stream.popsww.com'
            res=get('https://stream.popsww.com'+self.path,headers=myheader)
            self.send_response(res.status_code)
            # for k,v in res.headers.items():
            #     self.send_header(k,v)
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('content-type',res.headers['content-type'])
            # self.send_header('set-cookie',res.headers['set-cookie'])
            self.end_headers()
            self.wfile.write(res.content)
            # print(res.content)
    def do_POST(self):
        myheader=self.headers
        myheader['host']='stream.popsww.com'
        res=post('https://stream.popsww.com'+self.path,self.rfile.read(int(myheader['content-length'])),headers=myheader)
        self.send_response(res.status_code)
        # for k,v in res.headers.items():
        #     self.send_header(k,v)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('content-type',res.headers.get('content-type'))
        # self.send_header('set-cookie',res.headers['set-cookie'])
        self.end_headers()
        self.wfile.write(res.content)
    def do_OPTIONS(self):
        if self.path== "/v1/drm/keys?type=widevine":
            print(1)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('Access-Control-Allow-Headers','Content-Type')
            self.end_headers()
            self.wfile.write(b'123')
        else:
            myheader=self.headers
            myheader['host']='stream.popsww.com'
            res=options('https://stream.popsww.com'+self.path,self.rfile.read(int(myheader['content-length'])),headers=myheader)
            self.send_response(res.status_code)
            # for k,v in res.headers.items():
            #     self.send_header(k,v)
            self.send_header('Access-Control-Allow-Origin','*')
            self.send_header('content-type',res.headers['content-type'])
            # self.send_header('set-cookie',res.headers['set-cookie'])
            self.end_headers()
            self.wfile.write(res.content)
s=ThreadingHTTPServer(('',8081),mybackend)
print('Started server!')
s.serve_forever()