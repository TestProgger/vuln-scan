from enum import Enum

PARENT_NAME = "scanner"


class HandlersNames(Enum):
    PORT_SCANNER = "port_scanner"
    NSE_SCANNER = "nse_scanner"