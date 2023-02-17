from http.server import BaseHTTPRequestHandler
import requests
import uuid

from Logging import *

class FacadeImpl(BaseHTTPRequestHandler):
    def __init__(self, log_service, msg_service, *args, **kwargs):
        self.log_srv = log_service
        self.msg_srv = msg_service
        # BaseHTTPRequestHandler calls do_GET **inside** __init__ !!!
        # So we have to call super().__init__ after setting attributes.
        super().__init__(*args, **kwargs)

    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        # domain_log("GET request,\nPath: {0}\nHeaders:\n{1}".format( str(self.path), str(self.headers)))
        domain_log("GET request!")
        log_srv_messages = requests.get(url = self.log_srv)
        msg_srv_messages = requests.get(url = self.msg_srv)
        result = ""
        if not log_srv_messages.ok or not msg_srv_messages.ok:
            self._set_response(500)
            result = "log_srv returned " + str(log_srv_messages.status_code) + " msg_srv returned " + str(msg_srv_messages.status_code)
        else:
            self._set_response(200)
            result = log_srv_messages.content.decode('utf-8') + msg_srv_messages.content.decode('utf-8')
        self.wfile.write(result.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # domain_log("POST request,\nPath: {0}\nHeaders:\n{1}\n\nBody:\n{2}".format(
        #         str(self.path), str(self.headers), post_data.decode('utf-8')))
        domain_log("POST request! With new message: " + post_data.decode('utf-8'))

        header = {"ID": str(uuid.uuid1())}
        try:
            log_srv_response = requests.post(url = self.log_srv, headers=header, data=post_data)
            msg_srv_response = requests.post(url = self.msg_srv, headers=header, data=post_data)
        except Exception as e:
            self._set_response(500)
            self.wfile.write("No connection to interal services".encode('utf-8'))
            return

        result = ""
        if not log_srv_response.ok or not msg_srv_response.ok:
            self._set_response(500)
            result = "log_srv returned " + str(log_srv_response.status_code) + " msg_srv returned " + str(msg_srv_response.status_code)
            domain_log("ERROR: " + result)
        else:
            self._set_response(200)
            domain_log("Message writen with " + str(header))
        self.wfile.write(result.encode('utf-8'))