from threading import Lock


class AddressHelper():
    def __init__(self, logging_ports, message_ports) -> None:
        self.logging_mtx = Lock()
        self.logging_round_robin_index = 0
        self.logging_ch = []
        self.message_mtx = Lock()
        self.message_round_robin_index = 0
        self.message_ch = []
        for port in logging_ports:
            self.logging_ch.append("http://127.0.0.1:{}/".format(port))
        for port in message_ports:
            self.message_ch.append("http://127.0.0.1:{}/".format(port))

    def GetLoggingSvcAddress(self):
        with self.logging_mtx:
            ch = self.logging_ch[self.logging_round_robin_index]
            self.logging_round_robin_index += 1
            if self.logging_round_robin_index == len(self.logging_ch):
                self.logging_round_robin_index = 0
            return ch
    
    def GetMessageSvcAddress(self):
        with self.message_mtx:
            ch = self.message_ch[self.message_round_robin_index]
            self.message_round_robin_index += 1
            if self.message_round_robin_index == len(self.message_ch):
                self.message_round_robin_index = 0
            return ch
    