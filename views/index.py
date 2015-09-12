from models import User
from templates import render

class IndexView:
    def GET(self):
        return render.index()
