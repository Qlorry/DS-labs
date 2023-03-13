from http.server import HTTPServer
import argparse

import Constants as constants
from Constants import ConfigKeys
from FacadeImpl import *
from FacadeDomain import FacadeDomain
from AddressHelper import AddressHelper

class FacadeApp:
    def __init__(self):
        self.name = "facade-service"
        configure_logging(constants.SERVICE_NAME)

        self.arg_parser = argparse.ArgumentParser(
                    prog = constants.SERVICE_NAME,
                    description = 'Service to log messages')
        self.add_args_to_parser()
        
        self.config = dict()
        self.parse_args()

    def parse_args(self):
        args = self.arg_parser.parse_args()
        self.config[ConfigKeys.PORT] = args.port

    def add_args_to_parser(self):
        self.arg_parser.add_argument('-p', '--port', type=int) 

    def run(self):
        
        FacadeDomain(AddressHelper())

        server_address = ('', self.config[ConfigKeys.PORT])
        httpd = HTTPServer(server_address, FacadeImpl)
        app_log('Starting httpd at ' + str(server_address))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        app_log('Stopping httpd...')