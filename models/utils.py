class Pretty(object):
    @staticmethod
    def pos(pos):
        y, x = [ord(p) - 97 for p in pos]
        return '%s%s' % (
            'ABCDEFGHJKLMNOPQRST'[x],
            19 - y,
        )

    @staticmethod
    def rating(rating):
        if rating < 0:
            return "%dk" % (-rating,)
        else:
            return "%dd" % (rating,)
