from config.settings.env import env
import os

LOGGING_DIR = env.str('LOG_DIR', default='./logs')
LOGGING_FILE_SIZE = env.int('LOG_FILE_SIZE', default=100*2**20)

if not os.path.isdir(LOGGING_DIR):
    os.mkdir(LOGGING_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(module)s/%(levelname)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "file": {
            "format": "%(asctime)s | %(levelname)s | %(module)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "encoding": "UTF-8",
            "filename": os.path.join(LOGGING_DIR, 'app.log'),
            "maxBytes": LOGGING_FILE_SIZE,
            "backupCount": 4
        },
        "api_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "encoding": "UTF-8",
            "filename": os.path.join(LOGGING_DIR, 'api.log'),
            "maxBytes": LOGGING_FILE_SIZE,
            "backupCount": 4
        },
        "task_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "encoding": "UTF-8",
            "filename": os.path.join(LOGGING_DIR, 'task.log'),
            "maxBytes": LOGGING_FILE_SIZE,
            "backupCount": 4
        }

    },
    "loggers": {
        "project": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console", ],
            "level": "INFO",
            "propagate": False
        },
        "api": {
            "handlers": ["console", 'api_file'],
            "level": "INFO",
            "propagate": False
        },
        "task": {
            "handlers": ["console", "task_file"],
            "level": "INFO",
            "propagate": False
        }
    },
}