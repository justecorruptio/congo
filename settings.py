import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DATABASE = {
    'dbn': 'mysql',
    'db': 'congo',
    'user': 'root',
    'pw': '',
}

DEBUG = True

COOKIE_KEY_USER_ID = 'uid'
COOKIE_KEY_NONCE = 'nonce'
COOKIE_DOMAIN = 'localhost'

ADMINS = []

try:
    from settings_qa import *
except:
    pass

try:
    from settings_prod import *
except:
    pass

ADMINS = [x.lower() for x in ADMINS]
