from django.conf import settings

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2t_u+c$h1aer4&g6_yihg+phk!gt+_!g2=zm92zck%1%fx$=)x'

DATABASES = settings.DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'friday',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'friday_test',
        },
    }
}

TEST = True
DEBUG = True
