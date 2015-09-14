import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DATABASE = {
    'dbn': 'mysql',
    'db': 'congo',
    'user': 'go',
    'pw': '***REMOVED***',
}

DEBUG = True

COOKIE_KEY_USER_ID = 'uid'
COOKIE_KEY_NONCE = 'nonce'
COOKIE_DOMAIN = '***REMOVED***'

try:
    from settings_prod import *
except:
    pass
