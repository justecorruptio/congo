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
            where=where or None,
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

    @classmethod
    def update(cls, keys, **kwargs):
        not_keys = list(set(kwargs.keys()) - set(keys))

        criteria = dict((k, kwargs[k]) for k in keys)
        to_change = dict((k, kwargs[k]) for k in not_keys)

        result = cls.get(**criteria)

        if result:
            where = ' AND '.join(
                '%s=$%s' % (n, n)
                for n in keys
            )
            cls.db.update(
                cls.table_name,
                where,
                vars=criteria,
                **to_change
            )
            return True
        return False


    @classmethod
    def insert_or_update(cls, keys, **kwargs):
        if cls.update(keys, **kwargs):
            return True

        cls.insert(**kwargs)
        return False

