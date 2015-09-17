import json
import web

from views.utils import require_login
from models import (
    Player,
    Pretty,
    Vote,
)

class StatsView(object):
    @require_login
    def GET(self):
        game_id = web.ctx.game.id;
        players = Player.game_stats(game_id)
        num_players = len(players)

        black = []
        white = []
        for player in players:
            ([], black, white)[player.color].append('%s (%s)' % (
                player.name,
                Pretty.rating(player.rating),
            ))

        num_votes = Vote.game_stats(game_id)

        return json.dumps({
            'num_players': num_players,
            'num_votes': num_votes,
            'black_players': '<br>'.join(black),
            'white_players': '<br>'.join(white),
        })
