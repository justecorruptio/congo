import json
import time
import web

import settings
from forms import VoteForm
from models import (
    GameState,
    Pretty,
    Vote,
)
from views.utils import require_login

class GameStateView(object):

    @require_login
    def GET(self):
        now = time.localtime()
        hours_left = 23 - now.tm_hour
        mins_left = 59 - now.tm_min
        time_left = "%dh %dm." % (hours_left, mins_left)

        if web.ctx.game.your_turn:
            vote_counts = Vote.summary(web.ctx.game.id, web.ctx.game.current_seq)
            top_votes = [
                {
                    'pos': vote.move,
                    'count': int(vote.cnt),
                    'label': vote.move != 'tt' and chr(i + 65) or 'Pass',
                }
                for i, vote in enumerate(vote_counts)
            ]
        else:
            top_votes = []
        turn = web.ctx.game.current_seq % 2 == 1 and "Black" or "White"
        game_state = GameState.get(
            game_id=web.ctx.game.id,
            seq=web.ctx.game.current_seq - 1,
        )
        return json.dumps({
            'id': web.ctx.game.id,
            'current_seq': web.ctx.game.current_seq,
            'board_size': 19,
            'board': json.loads(game_state.board),
            'illegal': json.loads(game_state.illegal),
            'info': "<b>%d:</b> %s's turn. Captures: Black %s, White %s" % (
                web.ctx.game.current_seq,
                turn,
                game_state.black_captures,
                game_state.white_captures,
            ),
            'votes': top_votes,
            'time_left': time_left,
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
            ip_address=web.ctx.ip,
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
