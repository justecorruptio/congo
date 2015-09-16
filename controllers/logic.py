import json
import os
import re
import tempfile

from models import (
    Game,
    GameState,
    Pretty,
    Vote,
)

GNUGO_PATH = '/usr/games/gnugo'
DEFAULT_SGF = '(;GM[1]FF[4]SZ[19]KM[6.5]HA[0]RU[Japanese]PL[B])'

def call_gnugo(sgf, seq, move):
    color = seq % 2 == 1 and 'b' or 'w'

    sgf_file = tempfile.NamedTemporaryFile(
        mode='wb',
        dir='/tmp',
        prefix='congo_sgf_',
        suffix='.sgf',
    )

    sgf_file.write(sgf)
    sgf_file.flush()

    cmd = """
        printf 'play %s %s\\ncaptures b\\ncaptures w\\nprintsgf' |
        %s --mode=gtp -l %s
    """ % (
        color,
        Pretty.pos(move),
        GNUGO_PATH,
        sgf_file.name,
    )
    gnugo = os.popen(cmd)
    gnugo_result = gnugo.read()
    sgf_file.close()

    return gnugo_result


def parse_gnugo(result):
    parts = re.split(r'\s*=\s*', result, 4)
    black_captures = int(parts[2])
    white_captures = int(parts[3])
    sgf = parts[4]

    def find_pos_list(tag):
        match = re.search(tag + r'\s*((\[..\]\s*)+)', sgf)
        if not match:
            return []
        return re.findall('[a-t][a-t]', match.groups()[0])

    black_pos = find_pos_list('AB')
    white_pos = find_pos_list('AW')
    illegal = find_pos_list('IL')

    sgf = re.sub('(GN|DT|AP)\[.*?\]\s*', '', sgf)
    sgf = re.sub('KM\[.*?\]\s*', 'KM[6.5]', sgf)

    board = [[0] * 19 for i in xrange(19)]

    for x, y in black_pos:
        board[ord(y) - 97][ord(x) - 97] = 1

    for x, y in white_pos:
        board[ord(y) - 97][ord(x) - 97] = 2

    return {
        'black_captures': black_captures,
        'white_captures': white_captures,
        'illegal': json.dumps(illegal),
        'board': json.dumps(board),
        'sgf': sgf,
    }


def next_move():

    game = Game.current()
    last_state = GameState.get(
        game_id=game.id,
        seq=game.current_seq - 1
    )

    if last_state is None:
        GameState.insert(
            game_id=game.id,
            seq=0,
            black_captures=0,
            white_captures=0,
            illegal=json.dumps([]),
            board=json.dumps([[0] * 19] * 19),
            sgf=DEFAULT_SGF,
        )
        return True

    top_moves = Vote.summary(game.id, game.current_seq)
    if not top_moves:
        return False

    top_move = top_moves[0].move
    result = call_gnugo(
        last_state.sgf,
        game.current_seq,
        top_move,
    )

    next_state = parse_gnugo(result)

    GameState.insert(
        game_id=game.id,
        seq=game.current_seq,
        **next_state
    )

    Game.insert_or_update(
        keys=('id',),
        id=game.id,
        current_seq=game.current_seq + 1,
    )
