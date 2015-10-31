import web

import settings
from models import Session


def require_login(func):
    def func_wrapper(self, *args, **kwargs):
        if not Session.is_logged_in():
            raise web.notfound('unauthorized')

        Session.load_game_data()
        return func(self, *args, **kwargs)

    return func_wrapper


def is_admin():
    return web.ctx.user.name.lower() in settings.ADMINS


def require_admin(func):
    def func_wrapper(self, *args, **kwargs):
        if not is_admin():
            raise web.notfound('unauthorized')

        return func(self, *args, **kwargs)

    return func_wrapper

