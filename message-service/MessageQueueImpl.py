from threading import Thread
import hazelcast
import consul

from MessageDomain import MessageDomain
from Logging import *

class MessageQueueImpl():
    def __init__(self, hazelcast_addrs, queue_name):
        self.queue_name = queue_name #"logging-data-queue"
        self.hazel_addr = hazelcast_addrs

    def read_messages_async(self):
        th = Thread(target=self._read_messages)
        th.start()

    def _read_messages(self):
        client = hazelcast.HazelcastClient(cluster_members=self.hazel_addr)
        domain = MessageDomain()
        q = client.get_queue(self.queue_name)
        service_log("Strated queue reader")   
        while True:
            t = q.take().result()
            domain.add_message(t["id"], t["data"])
            
