from enum import Enum


class WorkerNames(Enum):
    SQL_INJECTION = "sql_injection"
    DIR_ENUMERATION = "dir_enumeration"
    SCAN = "scan"
    HTTP_ENUM = "http_enum"
