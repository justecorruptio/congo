import web

from forms import SignUpForm
from models import User
from templates import render

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
        created, err = User.create(
            form.d.name,
            form.d.passwd,
            rating=rating,
        )
        return "YO!"
