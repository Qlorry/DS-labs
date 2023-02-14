from http.server import HTTPServer
import argparse
from functools import partial

from FacadeImpl import *
from FacadeApp import *

CONFIG_KEY_PORT = "PORT"
CONFIG_KEY_LOG_SERVICE = "LOG_ADDR"
CONFIG_KEY_MSG_SERVICE = "MSG_ADDR"

class FacadeApp:
    def __init__(self):
        self.name = "facade-service"
        configure_logging(self.name)

        self.arg_parser = argparse.ArgumentParser(
                    prog = self.name,
                    description = 'Service to provide URLs for available DAS and other svcs')
        self.add_args_to_parser()
        
        self.config = dict()
        self.parse_args()

    def parse_args(self):
        args = self.arg_parser.parse_args()
        self.config[CONFIG_KEY_PORT] = args.port
        self.config[CONFIG_KEY_LOG_SERVICE] = args.log_service
        self.config[CONFIG_KEY_MSG_SERVICE] = args.message_service

    def add_args_to_parser(self):
        self.arg_parser.add_argument('-p', '--port', type=int) 
        self.arg_parser.add_argument('-ls', '--log-service', type=str) 
        self.arg_parser.add_argument('-ms', '--message-service', type=str) 


    def run(self):
        server_address = ('', self.config[CONFIG_KEY_PORT])
        handler = partial(FacadeImpl, self.config[CONFIG_KEY_LOG_SERVICE], self.config[CONFIG_KEY_MSG_SERVICE])
        httpd = HTTPServer(server_address, handler)
        app_log('Starting httpd at ' + str(server_address))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        app_log('Stopping httpd...')