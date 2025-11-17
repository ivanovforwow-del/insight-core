"""
Docker settings for InsightCore project.
This settings module is used when running the application in Docker containers.
It configures the application to use PostgreSQL instead of SQLite.
"""

import os
from pathlib import Path
from datetime import timedelta
from .settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration for Docker
# Use PostgreSQL when running in Docker container
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'insightcore'),
        'USER': os.getenv('POSTGRES_USER', 'insightcore_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'insightcore_password'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'OPTIONS': {
            'options': '-c default_transaction_isolation=serializable'
        },
    }
}

# Use the same SECRET_KEY as in the base settings
# or override it with environment variable if needed
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)

# Override DEBUG based on environment variable
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() == 'true'

# Allow all hosts in Docker environment
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0').split(',')

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3001",  # Frontend origin
]

CORS_ALLOW_CREDENTIALS = True

# Only allow all origins in debug mode, otherwise use specific allowed origins
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True