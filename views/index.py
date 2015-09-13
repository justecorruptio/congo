from models import (
    Session,
    User,
)
from templates import render

class IndexView(object):
    def GET(self):
        logged_in, user_id = Session.is_logged_in()
        if logged_in:
            return render.main()
        else:
            return render.index()
