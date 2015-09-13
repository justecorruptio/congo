import web

from models import (
    Game,
    Session,
)
from templates import render


class IndexView(object):
    def GET(self):
        if Session.is_logged_in():
            Session.load_game_data()
            return render.main()
        else:
            return render.index()
