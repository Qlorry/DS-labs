from http.server import HTTPServer
import argparse

from ConsulRepo import ConsulRepo

from MessageHttpImpl import *
from MessageQueueImpl import *
from MessageApp import *

CONFIG_KEY_PORT = "PORT"
CONFIG_KEY_CONSUL_ADDR = "CONSUL_ADDR"

class MessageApp:
    def __init__(self):
        self.name = "message-service"
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
        self.config[CONFIG_KEY_CONSUL_ADDR] = args.consul

    def add_args_to_parser(self):
        self.arg_parser.add_argument('-p', '--port', type=int, help="port to work on") 
        self.arg_parser.add_argument('-consul', type=str) 

    def run(self):
        c = ConsulRepo(self.name, self.config[CONFIG_KEY_PORT], self.config[CONFIG_KEY_CONSUL_ADDR])
        consumer = MessageQueueImpl(c.get_hazelcast_address(), c.get_queue_name())
        consumer.read_messages_async()
        
        server_address = ('', self.config[CONFIG_KEY_PORT])
        httpd = HTTPServer(server_address, MessageHttpImpl)
        app_log('Starting httpd at ' + str(server_address))
        c.register()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        app_log('Stopping httpd...')