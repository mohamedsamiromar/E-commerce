import os
from .settings import *  # noqa: F401, F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'test-secret-key-not-for-production'

# Disable django-heroku for tests (it adds sslmode which SQLite doesn't support)
os.environ.pop('DATABASE_URL', None)
