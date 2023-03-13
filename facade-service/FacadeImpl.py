from http.server import BaseHTTPRequestHandler

from Logging import *
from FacadeDomain import FacadeDomain

class FacadeImpl(BaseHTTPRequestHandler):
    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        responce_text = ""

        service_log("GET request!")
        domain = FacadeDomain()
        if self.path == "/":
            result = domain.get_messages()
            if result.status:
                self._set_response(200)
                responce_text = result.messages
            else:
                self._set_response(500)
                responce_text = "No connection to interal services"
        else:
            self._set_response(404)
        self.wfile.write(responce_text.encode('utf-8'))

    def do_POST(self):
        responce_text = ""

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        service_log("POST request! With new message: " + post_data.decode('utf-8'))

        domain = FacadeDomain()
        if self.path == "/":
            if domain.send_message_to_internals(post_data.decode('utf-8')):
                self._set_response(200)
            else:
                self._set_response(500)
                responce_text = "No connection to interal services"
        else:
            self._set_response(404)

        self.wfile.write(responce_text.encode('utf-8'))