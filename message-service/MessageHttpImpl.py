from http.server import BaseHTTPRequestHandler

from MessageDomain import MessageDomain

from Logging import *

class MessageHttpImpl(BaseHTTPRequestHandler):
    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def log_message(self, format, *args):
        return
    
    def do_GET(self):
        responce = ""
        domain = MessageDomain()
        res = domain.get_messages()
        service_log("GET request for path {}".format(self.path))
        responce = res
        self._set_response(200)
        self.wfile.write(responce.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        service_log("POST request for URI '{}'! With new message: {}".format(self.path, post_data.decode('utf-8')))
        self._set_response(501)
        self.wfile.write("".format(self.path).encode('utf-8'))