import json
import time
import web

import settings
from forms import VoteForm
from models import (
    Comment,
    GameState,
    Pretty,
    Vote,
    SystemMessage,
)
from views.utils import require_login

class GameStateView(object):

    @require_login
    def GET(self):
        now = time.localtime()
        hours_left = 23 - now.tm_hour
        mins_left = 59 - now.tm_min
        time_left = "%02d:%02d" % (hours_left, mins_left)

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
            comment_counts = Comment.summary(web.ctx.game.id, web.ctx.game.current_seq)
            comments = [
                {
                    'pos': comment.move,
                }
                for i, comment in enumerate(comment_counts)
            ]
        else:
            top_votes = []
            comments = []
        turn = web.ctx.game.current_seq % 2 == 1 and "Black" or "White"
        game_state = GameState.get(
            game_id=web.ctx.game.id,
            seq=web.ctx.game.current_seq - 1,
        )

        system_message = SystemMessage.get()
        if system_message:
            system_message = system_message.message

        return json.dumps({
            'id': web.ctx.game.id,
            'current_seq': web.ctx.game.current_seq,
            'board_size': 19,
            'board': json.loads(game_state.board),
            'last_move': game_state.move,
            'illegal': json.loads(game_state.illegal),
            'info': "<b>%d:</b> %s's turn. Captures: Black %s, White %s" % (
                web.ctx.game.current_seq,
                turn,
                game_state.black_captures,
                game_state.white_captures,
            ),
            'votes': top_votes,
            'comments': comments,
            'time_left': time_left,
            'system_message': system_message,
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


class CommentView(object):
    @require_login
    def POST(self):
        form = VoteForm()
        if not form.validates():
            raise web.notfound(form.note)
        if not web.ctx.game.your_turn:
            raise web.notfound("It's not your turn!")
        Comment.insert_or_update(
            ('game_id', 'user_id', 'seq', 'move'),
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
        comments = Comment.details(web.ctx.game.id, web.ctx.game.current_seq, pos)
        votes = Vote.details(web.ctx.game.id, web.ctx.game.current_seq, pos)

        all_comments = {}
        for c in comments:
            all_comments[(c.rating, c.name)] = (c.notes, 'comment')

        for v in votes:
            all_comments[(v.rating, v.name)] = (v.notes, 'vote')

        sorted_comments = sorted(
            all_comments.iteritems(),
            key=lambda ((rating, name), _): -rating,
        )

        return json.dumps({
            'display_pos': Pretty.pos(pos),
            'count': count,
            'votes': [
                {
                    'name': name,
                    'rating': Pretty.rating(rating),
                    'notes': notes,
                    'type': note_type,
                }
                for (rating, name), (notes, note_type) in sorted_comments
            ],
        })
