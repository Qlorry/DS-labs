import asyncio
from threading import Lock, Thread, Condition
import uuid

import hazelcast

from Logging import *


class MessageDomainMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MessageDomain(metaclass=MessageDomainMeta):
    def __init__(self):
        self.messages_mtx = Lock()
        self.messages = {}

    def add_message(self, id, message):
        with self.messages_mtx:
            self.messages[id] = message
        domain_log("Message {} added".format(id))

    def get_messages(self):
        res = ""
        with self.messages_mtx:
            for message in self.messages:
                res += self.messages[message] + '\n'
        domain_log("Retrieved {} messages".format(len(res)))
        return res

