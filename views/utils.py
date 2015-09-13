import web

from models import Session


def require_login(func):
    def func_wrapper(self, *args, **kwargs):
        if not Session.is_logged_in():
            raise web.notfound('unauthorized')

        Session.load_game_data()
        return func(self, *args, **kwargs)

    return func_wrapper
