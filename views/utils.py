import web

from models import Session


def require_login(func):
    def func_wrapper(self, *args, **kwargs):
        if Session.is_logged_in():
            return func(self, *args, **kwargs)
        else:
            raise web.notfound('unauthorized')
    return func_wrapper
