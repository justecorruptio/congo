import web

from forms import SignUpForm
from models import User
from templates import render

class SignUpView:

    def GET(self):
        form = SignUpForm()
        created, err = User.create('Andy', 'testpasswd')
        return render.sign_up()
