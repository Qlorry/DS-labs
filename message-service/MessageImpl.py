from http.server import BaseHTTPRequestHandler

from Logging import *

class MessageImpl(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        # domain_log("GET request,\nPath: %s\nHeaders:\n%s".format( str(self.path), str(self.headers)))
        domain_log("GET request")
        self._set_response()
        self.wfile.write("not implemented yet".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # domain_log("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s".format(
        #         str(self.path), str(self.headers), post_data.decode('utf-8')))
        domain_log("POST request")

        self._set_response()
        self.wfile.write(b'')