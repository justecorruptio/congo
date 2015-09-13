import web

from forms import (
    LoginForm,
    SignUpForm,
)
from models import (
    Session,
    User,
)
from templates import render

class LoginView(object):

    def POST(self):
        form = LoginForm()
        if not form.validates():
            raise web.notfound(form.note)

        authenticated, user, err = User.auth(form.d.name, form.d.passwd)
        if not authenticated:
            raise web.notfound(err)

        Session.login(user.id)

        return "YO!"


class LogoutView(object):

    def GET(self):
        Session.logout()
        raise web.seeother('/')


class SignUpView:

    def POST(self):
        form = SignUpForm()
        if not form.validates():
            raise web.notfound(form.note)
        if User.get(name=form.d.name):
            raise web.notfound('Name is already taken.')
        rating = int(form.d.rating[:-1])
        if form.d.rating[-1] in 'kK':
            rating = -rating
        created, user_id, err = User.create(
            form.d.name,
            form.d.passwd,
            rating=rating,
        )

        Session.login(user_id)

        return "YO!"
