import hashlib
import random
import string
import web

import settings
from models.base import Model


def gen_salt():
    return ''.join(
        random.choice(string.lowercase)
        for i in xrange(40)
    )


class User(Model):

    table_name = 'Users'

    @classmethod
    def create(cls, name, passwd, rating=-1):
        salt = gen_salt()
        passwd_hash = hashlib.sha1(salt + passwd + salt).hexdigest()

        user = cls.get(name=name)
        if user:
            return False, -1, "User already exists."

        user_id = cls.insert(
            name=name,
            rating=rating,
            salt=salt,
            passwd_hash=passwd_hash,
        )

        return True, user_id, ""

    @classmethod
    def auth(cls, name, passwd):
        user = cls.get(name=name)
        if not user:
            return False, None, "User not registered."

        salt = user.salt
        passwd_hash = hashlib.sha1(salt + passwd + salt).hexdigest()
        if passwd_hash != user.passwd_hash:
            return False, None, "Incorrect password."

        return True, user, ""
