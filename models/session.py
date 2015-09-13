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

        web.setcookie(
            settings.COOKIE_KEY_USER_ID,
            str(user_id),
            domain=settings.COOKIE_DOMAIN,
        )
        web.setcookie(
            settings.COOKIE_KEY_NONCE,
            nonce,
            domain=settings.COOKIE_DOMAIN,
        )

    @classmethod
    def logout(cls):
        web.setcookie(
            settings.COOKIE_KEY_USER_ID,
            '',
            expires=-1,
            domain=settings.COOKIE_DOMAIN,
        )
        web.setcookie(
            settings.COOKIE_KEY_NONCE,
            '',
            expires=-1,
            domain=settings.COOKIE_DOMAIN,
        )

    @classmethod
    def is_logged_in(cls):

        cookies = web.cookies()
        user_id = cookies.get(settings.COOKIE_KEY_USER_ID)
        nonce = cookies.get(settings.COOKIE_KEY_NONCE)
        if user_id is None:
            return False, None

        session = cls.get(user_id=user_id)
        session_nonce = json.loads(session.data).get('nonce')
        if nonce != session_nonce:
            return False, None

        return True, user_id
