from enum import Enum


class ResponseError(Enum):
    INVALID_LANGUAGE_VERSION = "Неподдерживаемая версия языка"
    SERVICES_NOT_FOUND = "Не найдено инструкций для исполнения"
    INVALID_SYNTAX ="Невалидный синтаксис файла"
    UNKNOWN_FILE_STRUCTURE = "Неизвестная структура файла"
    SCENARIO_ALREADY_EXISTS = "Сценарий уже существует"
    SCENARIO_NOT_FOUND = "Сценарий не найден"
    SCENARIO_WITH_THIS_NAME_ALREADY_EXISTS = "Сценарий с таким наименованием уже существует"
    UNKNOWN_ERROR = "Неизвестна ошибка"
