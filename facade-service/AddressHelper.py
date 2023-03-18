from threading import Lock
import time

import consul
from Logging import *

class AddressHelper():
    def __init__(self, consul_address) -> None:
        self.cons = consul.Consul(host=consul_address) 
        self.logging_mtx = Lock()
        self.logging_round_robin_index = 0
        self.message_mtx = Lock()
        self.message_round_robin_index = 0

    def _get_addr(self, name, retries, sleep):
        index = None
        data = None
        for i in range(retries):
            try:
                data = self.cons.catalog.service(name, index)
            except Exception as e:
                domain_log(f'Error occured while getting {name} address ' + str(e))
            if data == None:
                time.sleep(sleep)
        result = []
        for service in data[1]:
            result.append("http://{}:{}/".format(service["ServiceAddress"], service["ServicePort"]))
        domain_log(f'Found {name} with address ' + str(result))
        return result

    def GetLoggingSvcAddress(self):
        all = self._get_addr("logging-service", 5, 5)
        if len(all) == 0:
            return None
        with self.logging_mtx:
            if self.logging_round_robin_index >= len(all):
                self.logging_round_robin_index = 0
            ch = all[self.logging_round_robin_index]
            self.logging_round_robin_index += 1
            return ch

    def GetMessageSvcAddress(self):
        all = self._get_addr("message-service", 5, 5)
        if len(all) == 0:
            return None
        with self.message_mtx:
            if self.message_round_robin_index >= len(all):
                self.message_round_robin_index = 0
            ch = all[self.message_round_robin_index]
            self.message_round_robin_index += 1
            return ch
    
    def get_hazelcast_address(self):
        index = None
        data = None
        domain_log("Getting hazelcast address")
        while data == None:
            try:
                data = self.cons.catalog.service("hazelcast", index)
            except Exception as e:
                domain_log("Error occured while getting hazelcast address " + str(e))
            if data == None:
                time.sleep(5)
        result = []
        for service in data[1]:
            result.append("{}:{}".format(service["ServiceAddress"], service["ServicePort"]))
        domain_log("Hazelcast address acquired: " + str(result))
        return result