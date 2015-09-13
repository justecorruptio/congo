import settings
from models.base import Model


class Game(Model):

    STATUS_FINISHED = 20
    STATUS_RUNNING = 10

    table_name = 'Games'

    @classmethod
    def current(cls):
        return cls.get(
            status=cls.STATUS_RUNNING,
        )
