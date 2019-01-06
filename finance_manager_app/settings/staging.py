from .base_settings import *
import dj_database_url

ENVIRONMENT = 'staging'
DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com']
SECRET_KEY = 'SECRET_KEY'
DATABASES = {
    'default': dj_database_url.config(
        default='DATABASE_URL'
    )
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}