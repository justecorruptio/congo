#!/usr/bin/env bash

THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )

PYTHONPATH=$THIS_DIR:$PYTHONPATH \
python - <<EOS
import sys
from models.user import User
from models.game import Player, Game

game = Game.current()

WHITE, BLACK = 0,1
success, black1_id, error = User.create('black', 'black')
if not success: sys.exit(error)
Player.insert(
    game_id=game.id,
    user_id=black1_id,
    color=BLACK,
)

success, white1_id, error = User.create('white', 'white')
if not success: sys.exit(error)
Player.insert(
    game_id=game.id,
    user_id=white1_id,
    color=WHITE,
)



EOS
