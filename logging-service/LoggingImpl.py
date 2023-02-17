from http.server import BaseHTTPRequestHandler

from Logging import *

stored_messages = dict()

class LoggingImpl(BaseHTTPRequestHandler):
    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        # domain_log("GET request,\nPath: {0}\nHeaders:\n{1}".format( str(self.path), str(self.headers)))
        res = ""
        counter = 0
        for value in stored_messages:
            res += stored_messages[value] + "\n"
            counter += 1
        domain_log('POST request {0} messages sent'.format(counter))
        self._set_response(200)
        self.wfile.write(res.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # domain_log("POST request,\nPath: {0}\nHeaders:\n{1}\n\nBody:\n{2}".format(
        #         str(self.path), str(self.headers), post_data.decode('utf-8')))
        domain_log('POST request, message "{0}" logged with ID "{1}"'.format(post_data.decode('utf-8'), self.headers["ID"]))
        stored_messages[self.headers["ID"]] = post_data.decode('utf-8')

        self._set_response(200)
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))