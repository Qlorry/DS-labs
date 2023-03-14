from threading import Thread
import hazelcast

from MessageDomain import MessageDomain
from Logging import *

class MessageQueueImpl():
    def __init__(self):
        self.queue_name = "logging-data-queue"

    def read_messages_async(self):
        th = Thread(target=self._read_messages)
        th.start()

    def _read_messages(self):
        client = hazelcast.HazelcastClient(cluster_members=["127.0.0.1:21000"])
        domain = MessageDomain()
        q = client.get_queue("logging-data-queue")
        service_log("Strated queue reader")   
        while True:
            t = q.take().result()
            domain.add_message(t["id"], t["data"])
            
