import json
import web

from views.utils import require_login

class GameStateView(object):

    @require_login
    def GET(self):
        return json.dumps({
            'data': 'hello',
        })
