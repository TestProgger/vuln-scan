from enum import Enum


class ParentWorker(Enum):
    SCANNER = "scanner"
    WEB = "web"
    NETWORK = "network"
    OS = "os"
