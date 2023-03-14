import os
import subprocess
import signal
from http.server import HTTPServer
import argparse
from LoggingDomain import LoggingDomain

from LoggingImpl import *
from LoggingApp import *

CONFIG_KEY_PORT = "PORT"
CONFIG_KEY_HAZELCAST_PORT = "HZ_PORT"
CONFIG_KEY_HAZELCAST_ID = "HZ_ID"

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
        self.config[CONFIG_KEY_HAZELCAST_PORT] = self.config[CONFIG_KEY_PORT] + 1000

    def __del__(self):
        self.stop_hazelcast()

    def set_signals_callback(self):
        signal.signal(signal.SIGABRT, self.signal_callback)
        signal.signal(signal.SIGINT, self.signal_callback)
        signal.signal(signal.SIGKILL, self.signal_callback)

    def signal_callback(self):
        self.stop_hazelcast()

    def parse_args(self):
        args = self.arg_parser.parse_args()
        if args.port != None:
            self.config[CONFIG_KEY_PORT] = args.port

    def add_args_to_parser(self):
        self.arg_parser.add_argument('-p', '--port', type=int) 

    def run_hazelcast(self):
        app_log("Starting Hazelcast docker container")
        arguments = ["docker", "run", 
                         "-d", "--rm", 
                         "--network", "hazelcast-network", "-e", "HZ_CLUSTERNAME=dev", 
                         "-p", "{}:5701".format(self.config[CONFIG_KEY_HAZELCAST_PORT]),
                         "hazelcast/hazelcast:5.2.2"]
        if self.config[CONFIG_KEY_PORT] == 20000:
            arguments = ["docker", "run", 
                         "-d", "--rm", 
                         "--name", "main_logging",
                         "--network", "hazelcast-network", "-e", "HZ_CLUSTERNAME=dev", 
                         "-p", "{}:5701".format(self.config[CONFIG_KEY_HAZELCAST_PORT]),
                         "hazelcast/hazelcast:5.2.2"]
        output = ""      
        with subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
            try:
                output = p.stdout.read()
                code = p.wait()
            except:  # Including KeyboardInterrupt, wait handled that.
                p.kill()
        if code != 0:
            app_log("Can not start hazelcast: \n" + str(output))
            exit()
        app_log("Successfully started Hazelcast!")
        self.config[CONFIG_KEY_HAZELCAST_ID] = output.decode("utf-8").replace(" ", "").replace("\n", "")
    
    def stop_hazelcast(self):
        app_log("Stopping Hazelcast!")
        os.system("docker stop " + self.config[CONFIG_KEY_HAZELCAST_ID])

    def run(self):
        self.run_hazelcast()

        LoggingDomain("localhost:{}".format(self.config[CONFIG_KEY_HAZELCAST_PORT]))

        server_address = ('', self.config[CONFIG_KEY_PORT])
        httpd = HTTPServer(server_address, LoggingImpl)
        app_log('Starting httpd at ' + str(server_address))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        app_log('Stopping httpd...')