import web

import settings

db = web.database(**settings.DATABASE)


class Model(object):

    @classmethod
    def fetch(cls, order=None, limit=None, **kwargs):
        where = ' AND '.join(
            '%s=$%s' % (n, n)
            for n in kwargs
        )
        return db.select(
            cls.table_name,
            where=where,
            vars=kwargs,
        )

    @classmethod
    def get(cls, **kwargs):
        results = cls.fetch(limit=1, **kwargs)
        if len(results) == 0:
            return None
        else:
            return results[0]

    @classmethod
    def insert(cls, **kwargs):
        db.insert(
            cls.table_name,
            **kwargs
        )
        return True
