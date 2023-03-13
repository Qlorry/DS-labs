from threading import Lock


class AddressHelper():
    def __init__(self) -> None:
        self.logging_mtx = Lock()
        self.round_robin_index = 0
        self.logging_ch = ["http://127.0.0.1:20000/"]
        self.message_ch = "http://127.0.0.1:30000/"

    def GetLoggingSvcAddress(self):
        with self.logging_mtx:
            ch = self.logging_ch[self.round_robin_index]
            self.round_robin_index += 1
            if self.round_robin_index == len(self.logging_ch):
                self.round_robin_index = 0
            return ch
    
    def GetMessageSvcAddress(self):
        return self.message_ch