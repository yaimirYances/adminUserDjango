from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':get_secret('NAME'),
        'USER':get_secret('USER'),
        'PASSWORD':get_secret('PASSWORD'),
        'HOST':'localhost',
        'PORT':'5432',
    }
}

STATIC_URL = 'static/'

#Indicando a django donde esta la carpeta static
STATICFILES_DIRS = [BASE_DIR / "static"]
#print(STATICFILES_DIRS)

#archivo multimedias
MEDIA_URL = '/media/' #url de almacenamiento
MEDIA_ROOT = BASE_DIR / 'media'
#print(BASE_DIR / 'media')
