import re
import web

from models import (
    Pretty,
    Vote,
)
from views.utils import require_login

class SgfDownloadView(object):

    @require_login
    def GET(self):
        game_id = web.ctx.game.id

        web.header(
            'Content-Disposition',
            'attachment; filename="ConGo-game-%s.sgf"' % (game_id,),
        )
        web.header('Content-Type', 'application/x-go-sgf')

        data = [
            '(;GM[1]FF[4]CA[UTF-8]AP[ConGo:0.1]ST[2]',
            'RU[Japanese]SZ[19]KM[6.50]',
            'GN[ConGo Game %s]PW[White Team]PB[Black Team]' % (game_id,),
            'CP[2015 Jay Chan]RO[%s]' % (game_id),
        ]

        end_seq = web.ctx.game.current_seq + 1

        for seq in range(1, end_seq):
            vote_counts = Vote.summary(web.ctx.game.id, seq)
            show_current_move = seq < end_seq - 1 or web.ctx.game.your_turn

            if seq > 1:
                data.append(';%s[%s]' % (
                    (seq - 1) % 2 == 1 and 'B' or 'W',
                    prev_chosen_move,
                ))

            if show_current_move:
                data.append('LB')
            vote_data = []

            for i, vote in enumerate(vote_counts):
                label = chr(i + 65)
                if i == 0:
                    chosen_move = vote.move
                if vote.move != 'tt':
                    if show_current_move:
                        data.append('[%s:%s]' % (vote.move, label))
                    vote_data.append('%s: %s votes\n' % (label, vote.cnt))
                else:
                    vote_data.append('Pass: %s votes\n' % (vote.cnt,))

            if seq == 1:
                data.append('C[con-go.net\n\n')
            else:
                data.append('C[')
                votes = Vote.details(game_id, seq - 1, prev_chosen_move)
                for vote in votes:
                    data.append('%s (%s)\\: ' % (vote.name, Pretty.rating(vote.rating)))
                    notes = re.sub('\n', ' ', vote.notes)
                    notes = re.sub('\[', '(', notes)
                    notes = re.sub('\]', ')', notes)
                    notes = re.sub(r'\\', '\\\\', notes)
                    notes = re.sub(r':', '\\:', notes)
                    data.append(notes + '\n\n')
                data.append('\n')

            if show_current_move:
                data.extend(vote_data)
            data.append(']')
            prev_chosen_move = chosen_move

        data.append(')')

        return ''.join(data)
