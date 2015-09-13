import web

import settings


class Model(object):

    db = web.database(**settings.DATABASE)

    @classmethod
    def fetch(cls, order=None, limit=None, **kwargs):
        where = ' AND '.join(
            '%s=$%s' % (n, n)
            for n in kwargs
        )
        return cls.db.select(
            cls.table_name,
            where=where,
            vars=kwargs,
        )

    @classmethod
    def delete(cls, **kwargs):
        where = ' AND '.join(
            '%s=$%s' % (n, n)
            for n in kwargs
        )
        return cls.db.delete(
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
        return cls.db.insert(
            cls.table_name,
            **kwargs
        )
