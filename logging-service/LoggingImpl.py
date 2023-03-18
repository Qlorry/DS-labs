from http.server import BaseHTTPRequestHandler

from LoggingDomain import LoggingDomain

from Logging import *

class LoggingImpl(BaseHTTPRequestHandler):
    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def log_message(self, format, *args):
        return
    
    def do_GET(self):
        responce = ""
        domain = LoggingDomain()
        if self.path == "/":
            res = domain.get_messages()
            if not res[0]:
                responce = "No messages today :("
                self._set_response(500)
            else:
                service_log('POST request {0} messages sent'.format(res[1]))
                responce = res[1]
                self._set_response(200)
        elif self.path == "/health/":
            self._set_response(200)
            return
        self.wfile.write(responce.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        
        service_log('POST request, message "{0}" logged with ID "{1}"'.format(post_data.decode('utf-8'), self.headers["ID"]))
        domain = LoggingDomain()
        if domain.add_message(self.headers["ID"], post_data.decode('utf-8')):
            self._set_response(200)
        else:
            self._set_response(500)
        self.wfile.write("".format(self.path).encode('utf-8'))