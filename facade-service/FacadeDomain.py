import asyncio
from threading import Lock, Thread, Condition
import uuid

import requests
import hazelcast

from Logging import *
from AddressHelper import AddressHelper


class GetMessage():
    def __init__(self, result = False, messages = ""):
        self.status = result
        self.messages = messages


class MessageSheduler():
    def __init__(self):
        self.task_list = []
        self.loop = asyncio.new_event_loop()
        runner = Thread(target=self.start)
        runner.start()

    def start(self):
        self.loop.run_until_complete(self.runner())

    async def runner(self):
        while True:
            if len(self.task_list) == 0:
                await asyncio.sleep(1)
            else:
                await self.task_list.pop()

    def create_task(self, func, *args, **kwargs):
        task = self.loop.create_task(func(*args, **kwargs))
        self.task_list.append(task)
        return task


class FacadeDomainMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class FacadeDomain(metaclass=FacadeDomainMeta):
    def __init__(self, addr_helper: AddressHelper):
        self.addr_helper = addr_helper
        self.messages = []
        self.sheduler = MessageSheduler()
        self.hazelcast_client = hazelcast.HazelcastClient(cluster_members=["127.0.0.1:21000"])

    # TODO: add retry logic
    async def send_message(self, channel, id, message, notify_cond):
        result = False
        try:
            header = {"ID": str(id)}
            svc_response = requests.post(url = channel, headers=header, data=message.encode('utf-8'))
            if not svc_response.ok:
                raise Exception("Send to {} failed with error {}: {}".format(channel, svc_response.status_code + svc_response.reason))
            domain_log("Message '{}' sent to {}".format(id, channel))
            result = True
        except Exception as e:
            domain_log(str(e))
            result = False
        finally:
            with notify_cond:
                notify_cond.notify()
        return result

    async def send_message_to_queue(self, id, message, notify_cond):
        message_structure = {"id":id, "data": message}
        try:
            q = self.hazelcast_client.get_queue("logging-data-queue")
            if not q.add(message_structure).result():
                raise Exception("Can not add message {} to hazelcast queue!!!".format(id))
            result = True
            domain_log("Message {} added to hazelcast queue".format(id))
        except Exception as e:
            domain_log(e)
            result = False
        finally:
            with notify_cond:
                notify_cond.notify()
                return result

    async def retrieve_message(self, channel, notify_cond):
        result = GetMessage()
        try:
            svc_response = requests.get(url = channel)
            if not svc_response.ok:
                raise Exception("Retrieve from {} failed with error {}: {}".format(channel, svc_response.status_code + svc_response.reason))
            domain_log("Retrieve messages from '{}' successfully".format(channel))

            result.status = True
            result.messages = svc_response.content.decode('utf-8')
        except Exception as e:
            domain_log(str(e))
            result.status = False
        finally:
            with notify_cond:
                notify_cond.notify()
        return result

    def send_message_to_internals(self, message):
        background_tasks = set()   
        condition = Condition()
        message_id = uuid.uuid1()

        logging_task = self.sheduler.create_task(self.send_message, 
                                         self.addr_helper.GetLoggingSvcAddress(), 
                                         message_id, message, 
                                         condition)
        background_tasks.add(logging_task)
        message_task = self.sheduler.create_task(self.send_message_to_queue, 
                                         message_id, message, 
                                         condition)
        background_tasks.add(message_task)

        while len(background_tasks) > 0:
            with condition:
                condition.wait(timeout=10)
                tasks_to_remove = []

                for task in background_tasks: 
                    if not task.done():
                        continue
                    if not task.result():
                        return False
                    tasks_to_remove.append(task)
                    
                for task in tasks_to_remove:
                    background_tasks.remove(task)

        return True

    def get_messages(self):
        background_tasks = set()   
        condition = Condition()
        result = GetMessage()

        logging_task = self.sheduler.create_task(self.retrieve_message, 
                                         self.addr_helper.GetLoggingSvcAddress(), 
                                         condition)
        background_tasks.add(logging_task)
        message_task = self.sheduler.create_task(self.retrieve_message, 
                                         self.addr_helper.GetMessageSvcAddress(), 
                                         condition)
        background_tasks.add(message_task)

        while len(background_tasks) > 0:
            with condition:
                condition.wait(timeout=10)
                tasks_to_remove = []

                for task in background_tasks: 
                    if not task.done():
                        continue
                    task_data : GetMessage = task.result()
                    if not task_data.status:
                        result.status = False
                        return result
                    result.status = True
                    result.messages += task_data.messages
                    tasks_to_remove.append(task)
                
                for task in tasks_to_remove:
                    background_tasks.remove(task)

        return result
