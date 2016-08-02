#!/usr/bin/env bash

THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )

PYTHONPATH=$THIS_DIR:$PYTHONPATH \
python -c 'from models.game import Game; Game.insert(status=Game.STATUS_RUNNING)'
