from probemanager.settings.base import *  # noqa
from cryptography.fernet import Fernet
import configparser
import ast
import os


config = configparser.ConfigParser()
config.read(os.path.join(ROOT_DIR, 'conf.ini'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

HOST = config['DEFAULT']['HOST']
ALLOWED_HOSTS = [HOST, 'localhost', '127.0.0.1']
GIT_BINARY = config['GIT']['GIT_BINARY']

# Specific for installation
PROJECT_NAME = 'probemanager'
APACHE_PORT = 80

with open(os.path.join(ROOT_DIR, 'secret_key.txt'), encoding='utf_8') as f:
    SECRET_KEY = f.read().strip()
with open(os.path.join(ROOT_DIR, 'fernet_key.txt'), encoding='utf_8') as f:
    FERNET_KEY = bytes(f.read().strip(), 'utf-8')

if os.path.isfile(os.path.join(BASE_DIR, 'version.txt')):
    with open(os.path.join(BASE_DIR, 'version.txt'), encoding='utf_8') as f:
        VERSION = f.read().strip()
else:
    VERSION = ""


def decrypt(cipher_text):
    fernet_key = Fernet(FERNET_KEY)
    if isinstance(cipher_text, bytes):
        return fernet_key.decrypt(cipher_text).decode('utf-8')
    else:
        return fernet_key.decrypt(cipher_text.encode('utf-8')).decode('utf-8')


if os.path.isfile(os.path.join(ROOT_DIR, 'password_db.txt')):
    with open(os.path.join(ROOT_DIR, 'password_db.txt'), encoding='utf_8') as f:
        PASSWORD_DB = decrypt(f.read().strip())
else:
    PASSWORD_DB = "probemanager"

# Celery settings
CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'probemanager',
        'USER': 'probemanager',
        'PASSWORD': PASSWORD_DB,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

SPECIFIC_APPS = ast.literal_eval(config['APPS']['PROD_APPS'])
INSTALLED_APPS = BASE_APPS + SPECIFIC_APPS

for app in SPECIFIC_APPS:
    LOGGING['loggers'].update({app: {'handlers': ['file', 'file-error'], 'propagate': True}})
    if os.path.isfile(BASE_DIR + "/" + app + "/settings.py"):
        exec(open(BASE_DIR + "/" + app + "/settings.py", encoding='utf_8').read())

LOGGING['handlers']['file'].update({'filename': config['LOG']['FILE_PATH']})
LOGGING['handlers']['file-error'].update({'filename': config['LOG']['FILE_ERROR_PATH']})

TIME_ZONE = config['DEFAULT']['TIME_ZONE']

if not os.path.isfile(os.path.join(BASE_DIR, 'core/fixtures/test-core-secrets.ini')):
    EMAIL_HOST = config['EMAIL']['EMAIL_HOST']
    EMAIL_PORT = int(config['EMAIL']['EMAIL_PORT'])
    EMAIL_HOST_USER = config['EMAIL']['EMAIL_HOST_USER']
    DEFAULT_FROM_EMAIL = config['EMAIL']['DEFAULT_FROM_EMAIL']
    EMAIL_USE_TLS = config.getboolean('EMAIL', 'EMAIL_USE_TLS')
    if os.path.isfile(os.path.join(ROOT_DIR, 'password_email.txt')):
        with open(os.path.join(ROOT_DIR, 'password_email.txt'), encoding='utf_8') as f:
            EMAIL_HOST_PASSWORD = decrypt(f.read().strip())
    elif config.has_option('EMAIL','EMAIL_HOST_PASSWORD'):
        EMAIL_HOST_PASSWORD = config['EMAIL']['EMAIL_HOST_PASSWORD']
    else:
        EMAIL_HOST_PASSWORD = ""
