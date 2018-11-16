"""
Django settings for britecore_application project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from .settings import *
SECRET_KEY = os.getenv('SECRET_KEY', None)

DEBUG = False
# Setting it to * because we don't know the IP we'll get with 
# zappa or docker deployments. I wouldn't use this in a real
# production environment
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': os.getenv("SQL_ENGINE", 'django.db.backends.sqlite3'),
        'NAME': os.getenv('SQL_DB', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.getenv('SQL_USER', 'user'),
        'PASSWORD': os.getenv('SQL_PASSWORD', 'password'),
        'HOST': os.getenv('SQL_HOST', 'localhost'),
        'PORT': os.getenv('SQL_PORT', '5432'),
    }
}