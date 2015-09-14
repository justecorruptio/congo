#!/usr/bin/env bash

THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )

PYTHONPATH=$THIS_DIR:$PYTHONPATH \
python -c 'from controllers.logic import next_move; next_move()'
