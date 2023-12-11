from enum import Enum


class ResponseError(Enum):
    INVALID_LANGUAGE_VERSION = "Неподдерживаемая версия языка"
    SERVICES_NOT_FOUND = "Не найдено инструкций для исполнения"
    INVALID_SYNTAX ="Невалидный синтаксис файла"
    UNKNOWN_FILE_STRUCTURE = "Неизвестная структура файла"
