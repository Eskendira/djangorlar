from .base import *

# Register local apps for this project
INSTALLED_APPS = INSTALLED_APPS + [
    'apps.abstracts',
    'apps.education',
]

# Custom user model
AUTH_USER_MODEL = 'auths.CustomUser'
