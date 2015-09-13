import web

from models import (
    Game,
    Session,
)
from templates import render


class IndexView(object):
    def GET(self):
        print Game.current().id
        if Session.is_logged_in():
            return render.main()
        else:
            return render.index()
