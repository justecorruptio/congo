import json
import web

from forms import VoteForm
from models import (
    Vote,
)
from views.utils import require_login

class GameStateView(object):

    @require_login
    def GET(self):
        return json.dumps({
            'id': 1,
            'board_size': 19,
            'board': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            'illegal': ['bb', 'cs'],
            'info': "Black's turn. Captures: Black 3, White 7",
            'votes': [
                {'pos': 'dd', 'count': 72, 'label': 'A'},
                {'pos': 'pd', 'count': 23, 'label': 'B'},
                {'pos': 'pp', 'count': 12, 'label': 'C'},
                {'pos': 'dc', 'count': 5, 'label': 'D'},
                {'pos': 'eg', 'count': 4, 'label': 'E'},
                {'pos': 'pf', 'count': 2, 'label': 'F'},
                {'pos': 'jj', 'count': 1, 'label': 'G'},
            ],
        })


class VoteView(object):
    @require_login
    def POST(self):
        form = VoteForm()
        if not form.validates():
            raise web.notfound(form.note)
        if web.ctx.game.current_seq % 2 != web.ctx.game.player_color % 2:
            raise web.notfound("It's not your turn!")
        Vote.insert_or_update(
            ('game_id', 'user_id', 'seq'),
            game_id=web.ctx.game.id,
            user_id=web.ctx.user.id,
            seq=web.ctx.game.current_seq,
            move=form.d.pos,
            notes=form.d.notes,
        )



class GameVotesView(object):
    @require_login
    def GET(self, pos):
        return json.dumps({
            'count': 13,
            'votes': [
                {'name': 'Bob', 'rating': '2D', 'notes': """
                    This is a standard way to reduce the side
                    of the board so that the opponent is weakened.
                """},
                {'name': 'Tom', 'rating': '7k', 'notes': """
                    Who care why this is good. It is a Hote move.
                """},
                {'name': 'Max', 'rating': '12k', 'notes': """
                    I'm a very dilligent writer who writes very long
                    things about anything although I usually nver really
                    make any sense at all an i mispell things.
                """},
            ],
        })
