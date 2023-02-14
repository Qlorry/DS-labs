from http.server import HTTPServer
import argparse

from LoggingImpl import *
from LoggingApp import *

CONFIG_KEY_PORT = "PORT"

class LoggingApp:
    def __init__(self):
        self.name = "logging-service"
        configure_logging(self.name)

        self.arg_parser = argparse.ArgumentParser(
                    prog = self.name,
                    description = 'Service to provide URLs for available DAS and other svcs')
        self.add_args_to_parser()
        
        self.config = dict()
        self.parse_args()

    def parse_args(self):
        args = self.arg_parser.parse_args()
        if args.port != None:
            self.config[CONFIG_KEY_PORT] = args.port

    def add_args_to_parser(self):
        self.arg_parser.add_argument('-p', '--port', type=int) 

    def run(self):
        server_address = ('', self.config[CONFIG_KEY_PORT])
        httpd = HTTPServer(server_address, LoggingImpl)
        app_log('Starting httpd at ' + str(server_address))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        app_log('Stopping httpd...')