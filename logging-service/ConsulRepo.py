import uuid
import socket

import consul

from Logging import *

class ConsulRepo():
    def __init__(self, service, service_port, consul_url):
        self.addr = consul_url
        self.my_name = service
        self.my_port = service_port
        self.my_service_id = str(uuid.uuid1())

    def register(self):
        ip = socket.gethostbyname(socket.gethostname())
        domain_log("Using ip {} to register {} with id {}".format(ip, self.my_name, self.my_service_id))
        while True:
            try:
                c = consul.Consul(host=self.addr)
                ip = socket.gethostbyname(socket.gethostname())
                check = consul.Check.http("http://{}:{}/health/".format(ip, self.my_port), "10s", "5s", deregister="20s")
                res = c.agent.service.register(self.my_name, port=self.my_port, address=ip, check=check, service_id=self.my_service_id)
                if res:
                    return
                domain_log("Service register failed")
            except Exception as e:
                domain_log(str(e))
            time.sleep(5)

    def unregister(self):
        try:
            c = consul.Consul(host=self.addr)
            domain_log("Unregistering {} from consul(id {})".format(self.my_name, self.my_service_id))
            c.agent.service.deregister(self.my_service_id)
        except Exception as e:
            domain_log(str(e))
    
    def get_hazelcast_address(self):
        c = consul.Consul(host=self.addr) 
        index = None
        data = None
        domain_log("Getting hazelcast address")
        while data == None:
            try:
                data = c.catalog.service("hazelcast", index)
            except Exception as e:
                domain_log("Error occured while getting hazelcast address " + str(e))
            if data == None:
                time.sleep(5)
        result = []
        for service in data[1]:
            result.append("{}:{}".format(service["ServiceAddress"], service["ServicePort"]))
        domain_log("Hazelcast address accuired: " + str(result))
        return result
    
    def get_map_name(self):
        c = consul.Consul(host=self.addr) 
        index = None
        data = None
        domain_log("Getting name for hazelcast map")
        while data == None:
            try:
                index, data = c.kv.get("map-name", index=index)
            except Exception as e:
                domain_log("Error occured while getting map-name " + str(e))
            if data == None:
                time.sleep(5)
        result = data['Value'].decode("utf-8") 
        domain_log(f'Name for hazelcast map is {result}')
        return result