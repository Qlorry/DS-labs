import os
import subprocess
import signal
from http.server import HTTPServer
import argparse
import consul
from ConsulRepo import ConsulRepo

from LoggingDomain import LoggingDomain
from LoggingImpl import *
from LoggingApp import *

CONFIG_KEY_PORT = "PORT"
CONFIG_KEY_CONSUL_ADDR = "CONSUL_ADDR"


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

    def __del__(self):
        self.consul.unregister()
        # self.stop_hazelcast()
        pass

    def set_signals_callback(self):
        signal.signal(signal.SIGABRT, self.signal_callback)
        signal.signal(signal.SIGINT, self.signal_callback)
        signal.signal(signal.SIGKILL, self.signal_callback)

    def signal_callback(self):
        self.consul.unregister()
        # self.stop_hazelcast()
        pass

    def parse_args(self):
        args = self.arg_parser.parse_args()
        if args.port != None:
            self.config[CONFIG_KEY_PORT] = args.port
        self.config[CONFIG_KEY_CONSUL_ADDR] = args.consul

    def add_args_to_parser(self):
        self.arg_parser.add_argument('-p', '--port', type=int) 
        self.arg_parser.add_argument('-consul', type=str) 

    # def run_hazelcast(self):
    #     app_log("Starting Hazelcast docker container")
    #     arguments = ["docker", "run", 
    #                      "-d", "--rm", 
    #                      "--network", "hazelcast-network", "-e", "HZ_CLUSTERNAME=dev", 
    #                      "-p", "{}:5701".format(self.config[CONFIG_KEY_HAZELCAST_PORT]),
    #                      "hazelcast/hazelcast:5.2.2"]
    #     if self.config[CONFIG_KEY_PORT] == 20000:
    #         arguments = ["docker", "run", 
    #                      "-d", "--rm", 
    #                      "--name", "main_logging",
    #                      "--network", "hazelcast-network", "-e", "HZ_CLUSTERNAME=dev", 
    #                      "-p", "{}:5701".format(self.config[CONFIG_KEY_HAZELCAST_PORT]),
    #                      "hazelcast/hazelcast:5.2.2"]
    #     output = ""      
    #     with subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
    #         try:
    #             output = p.stdout.read()
    #             code = p.wait()
    #         except:  # Including KeyboardInterrupt, wait handled that.
    #             p.kill()
    #     if code != 0:
    #         app_log("Can not start hazelcast: \n" + str(output))
    #         exit()
    #     app_log("Successfully started Hazelcast!")
    #     self.config[CONFIG_KEY_HAZELCAST_ID] = output.decode("utf-8").replace(" ", "").replace("\n", "")
    
    # def stop_hazelcast(self):
    #     app_log("Stopping Hazelcast!")
    #     os.system("docker stop " + self.config[CONFIG_KEY_HAZELCAST_ID])

    def run(self):
        self.consul = ConsulRepo(self.name, self.config[CONFIG_KEY_PORT], self.config[CONFIG_KEY_CONSUL_ADDR])
        
        LoggingDomain(self.consul.get_hazelcast_address(), self.consul.get_map_name())

        server_address = ('', self.config[CONFIG_KEY_PORT])
        httpd = HTTPServer(server_address, LoggingImpl)
        self.consul.register()

        app_log('Starting httpd at ' + str(server_address))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        app_log('Stopping httpd...')