import web

from models import (
    Session,
    User,
)
from templates import render

class IndexView(object):
    def GET(self):
        if Session.is_logged_in():
            return render.main()
        else:
            return render.index()
