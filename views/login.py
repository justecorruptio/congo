import web

from forms import LoginForm
from models import User
from models import Session
from templates import render

class LoginView:

    def POST(self):
        form = LoginForm()
        if not form.validates():
            raise web.notfound(form.note)

        authenticated, user, err = User.auth(form.d.name, form.d.passwd)
        if not authenticated:
            raise web.notfound(err)

        Session.login(user.id)

        return "YO!"
