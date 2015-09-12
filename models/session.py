import json
import random
import string
import web

import settings
from models.base import Model


def gen_nonce():
    return ''.join(
        random.choice(string.lowercase)
        for i in xrange(40)
    )


class Session(Model):

    table_name = 'Sessions'

    @classmethod
    def login(cls, user_id):
        cls.delete(user_id=user_id)

        nonce = gen_nonce()
        cls.insert(
            user_id=user_id,
            data=json.dumps({
                'nonce': nonce
            }),
        )

        web.setcookie('uid', str(user_id), domain=settings.COOKIE_DOMAIN)
        web.setcookie('nonce', nonce, domain=settings.COOKIE_DOMAIN)
