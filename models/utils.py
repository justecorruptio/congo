import os
import random

import settings


class Pretty(object):
    @staticmethod
    def pos(pos):
        if pos == 'tt':
            return 'Pass'

        x, y = [ord(p) - 97 for p in pos]
        return '%s%s' % (
            'ABCDEFGHJKLMNOPQRST'[x],
            19 - y,
        )

    @staticmethod
    def rating(rating):
        if rating is None:
            return "?"
        if rating < 0:
            return "%dk" % (-rating,)
        else:
            return "%dd" % (rating,)


class Version(object):
    try:
        version = open(os.path.join(
            settings.BASE_DIR,
            '.git/refs/heads/master',
        ), 'r').read()[:6]
    except:
        version = str(random.randint(100000, 999999))
