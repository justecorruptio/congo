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
            return False

        sessions = cls.db.query("""
            SELECT s.data as data, u.name as name, u.id as id
            FROM Sessions s JOIN Users u ON u.id = s.user_id
            WHERE s.user_id=$user_id
            LIMIT 1
        """, vars={'user_id': user_id})

        if not sessions:
            return False

        session = sessions[0]
        session_nonce = json.loads(session.data).get('nonce')
        if nonce != session_nonce:
            return False

        # user-like object
        web.ctx.user = session

        return True

    @classmethod
    def load_game_data(cls):
        user_id = web.ctx.user.id

        game = cls.db.query("""
            SELECT
                g.id AS id,
                g.current_seq AS current_seq,
                p.color AS player_color,
                IF(g.current_seq % 2 = p.color % 2, 1, 0) AS your_turn,
                v.move AS voted_move
            FROM Games g
            JOIN Players p
                ON p.game_id = g.id
            LEFT JOIN Votes v
                ON v.game_id = g.id
                AND v.user_id = p.user_id
                AND v.seq = g.current_seq
            WHERE g.status = 10
            AND p.user_id = $user_id
            LIMIT 1
        """, vars={'user_id': user_id})

        web.ctx.game = game[0]
