from threading import Lock


class AddressHelper():
    def __init__(self, logging_ports, message_port) -> None:
        self.logging_mtx = Lock()
        self.round_robin_index = 0
        self.logging_ch = []
        for port in logging_ports:
            self.logging_ch.append("http://127.0.0.1:{}/".format(port))
        self.message_ch = "http://127.0.0.1:{}/".format(message_port)

    def GetLoggingSvcAddress(self):
        with self.logging_mtx:
            ch = self.logging_ch[self.round_robin_index]
            self.round_robin_index += 1
            if self.round_robin_index == len(self.logging_ch):
                self.round_robin_index = 0
            return ch
    
    def GetMessageSvcAddress(self):
        return self.message_ch