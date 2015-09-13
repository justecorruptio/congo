from models import User
from templates import render

class IndexView(object):
    def GET(self):
        return render.index()
