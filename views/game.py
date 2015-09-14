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
        if web.ctx.game.your_turn:
            vote_counts = Vote.summary(web.ctx.game.id, web.ctx.game.current_seq)
            top_votes = [
                {
                    'pos': vote.move,
                    'count': int(vote.cnt),
                    'label': chr(i + 65),
                }
                for i, vote in enumerate(vote_counts)
            ]
        else:
            top_votes = []
        turn = web.ctx.game.current_seq == 1 and "Black" or "White"
        return json.dumps({
            'id': web.ctx.game.id,
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
            'info': "%s's turn. Captures: Black 3, White 7" % (turn,),
            'votes': top_votes,
        })


class VoteView(object):
    @require_login
    def POST(self):
        form = VoteForm()
        if not form.validates():
            raise web.notfound(form.note)
        if not web.ctx.game.your_turn:
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
