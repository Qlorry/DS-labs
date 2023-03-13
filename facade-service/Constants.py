from enum import Enum, unique

SERVICE_NAME = "facade-service"

@unique
class ConfigKeys(Enum):
    PORT = "PORT"
    LOGGING_SVC_PORTS = "LOGGING_SVC_PORTS"
    MESSAGE_SVC_PORTS = "MESSAGE_SVC_PORTS"

