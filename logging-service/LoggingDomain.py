import asyncio
from threading import Lock, Thread, Condition
import uuid

import hazelcast

from Logging import *


class LoggingDomainMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class LoggingDomain(metaclass=LoggingDomainMeta):
    def __init__(self, hazelcast_address, data_map):
        try:
            self.hz_client = hazelcast.HazelcastClient(
                cluster_members=hazelcast_address)
        except Exception as e:
            print(e)
        self.map_name = data_map #"logging-data-map"

    def add_message(self, id, message):
        try:
            data_map = self.hz_client.get_map(self.map_name)
            data_map.set(id, message).result()
            domain_log("Message {} sent to Hazelcast".format(id))
            return True
        except Exception as e:
            domain_log("Sending message to Hazelcast failed with error: " + str(e))
            return False

    def get_messages(self):
        res = ""
        try:
            data_map = self.hz_client.get_map(self.map_name)
            for message in data_map.values().result():
                res += message + '\n'
            domain_log("Retrieved {} messages from Hazelcast".format(len(res)))
            return (True, res)
        except Exception as e:
            domain_log("Retrieving messages from Hazelcast failed with error: " + str(e))
            return (False, "")
