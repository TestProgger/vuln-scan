from enum import Enum


class UserRole(Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    OPERATOR = "OPERATOR"
    USER = "USER"


class ResponseError(Enum):
    INVALID_USERNAME_OR_PASSWORD = "Неверный логин или пароль"
    INVALID_REFRESH_TOKEN = "Невалидный токен"