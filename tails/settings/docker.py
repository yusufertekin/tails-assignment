from tails.settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tails',
        'USER': 'root',
        'HOST': 'db',
        'PASSWORD': 'password',
        'PORT': 5432,
    }
}
