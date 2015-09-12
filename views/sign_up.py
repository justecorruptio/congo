import web

from models import User
from templates import render

class SignUp:
    def GET(self):
        created, err = User.create('Andy', 'testpasswd')
        return render.index(err)
