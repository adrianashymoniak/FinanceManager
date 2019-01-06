from .base_settings import *
import dj_database_url

ENVIRONMENT = 'production'
DEBUG = False
ALLOWED_HOSTS = ['.herokuapp.com']
SECRET_KEY = 'SECRET_KEY'
DATABASES = {
    'default': dj_database_url.config(
        default='DATABASE_URL'
    )
}
