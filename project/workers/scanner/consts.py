from enum import Enum


class WorkersNames(Enum):
    PORT_SCANNER = "port_scanner"
    NSE_SCANNER = "nse_scanner"


class NmapScriptKey(Enum):
    IDS = "ids"
    VULNERS = "vulners"


class NmapTableElemKey(Enum):
    ID = "id"
    IS_EXPLOIT = "is_exploit"
    CVSS = "cvss"
    TYPE = "type"