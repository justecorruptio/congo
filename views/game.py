import json
import web

from forms import VoteForm
from models import (
    Pretty,
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
        count = Vote.count(web.ctx.game.id, web.ctx.game.current_seq, pos)
        votes = Vote.details(web.ctx.game.id, web.ctx.game.current_seq, pos)
        return json.dumps({
            'display_pos': Pretty.pos(pos),
            'count': count,
            'votes': [
                {
                    'name': vote.name,
                    'rating': Pretty.rating(vote.rating),
                    'notes': vote.notes,
                }
                for vote in votes
            ],
        })
