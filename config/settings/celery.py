from config.settings.env import env

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND")
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"