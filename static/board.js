$(function() {

    function redraw_board(data) {
        var $sgf_board = $('.sgf-board');
        var board_size = data['board_size'];
        var board_data = data['board'];
        $sgf_board.empty();
        for(var i = 0; i < board_size; i++) {
            var $sgf_row = $('<div class="sgf-row"></div>');
            for(var j = 0; j < board_size; j++) {
                var $sgf_point = $('<div class="sgf-point"></div>');

                if(
                    (i == 3 || i == 9 || i == 15) &&
                    (j == 3 || j == 9 || j == 15)
                ) {
                    var $hoshi = $('<div class="sgf-hoshi"></div>');
                    $sgf_point.append($hoshi);
                }

                var color = board_data[i][j];
                var pos = String.fromCharCode(97 + i, 97 + j);
                $sgf_point.addClass({
                    0: 'sgf-empty',
                    1: 'sgf-black',
                    2: 'sgf-white'
                }[color]);
                var $sgf_cell = $('<div class="sgf-cell"></div>');
                $sgf_cell.data('pos', pos);
                $sgf_cell.addClass('sgf-cell-' + pos);
                $sgf_cell.append($sgf_point);
                $sgf_cell.click(function() {
                    var pos = $(this).data('pos');
                    start_vote(pos);
                });
                $sgf_row.append($sgf_cell);
            }
            $sgf_board.append($sgf_row);
        }

        var board_illegals = data['illegal'];
        for(var i = 0; i < board_illegals.length; i++) {
            var $sgf_cell = $('.sgf-cell-' + board_illegals[i]);
            $sgf_cell.data('illegal', true);
            var $sgf_point = $sgf_cell.find('.sgf-point')
            $sgf_point.attr('point-label', "\u25A2");
            $sgf_point.addClass('sgf-coord');
        }

        var board_votes = data['votes'];
        for(var i = 0; i < board_votes.length; i++) {
            var vote = board_votes[i];
            var $sgf_cell = $('.sgf-cell-' + vote.pos);
            var $sgf_point = $sgf_cell.find('.sgf-point')
            $sgf_point.attr('point-label', vote.label)
            $sgf_point.addClass('sgf-coord');
        }

        var $board_info = $('.congo-board-info');
        $board_info.text(data['info']);
    }

    function redraw_data_pane(data) {
        var $votes_table = $('.congo-votes-table');
        $votes_table.empty()

        var board_votes = data['votes'];
        for(var i = 0; i < board_votes.length; i++) {
            var vote = board_votes[i];
            var $tr = $('<tr>' +
                '<td><a href="" data-pos="' + vote.pos + '"' +
                ' class="data-pane-label">' + vote.label + '</a></td>' +
                '<td>' + vote.count + ' votes</td>' +
            '</tr>');
            $votes_table.append($tr);

            $('.data-pane-label').click(function(event) {
                event.preventDefault();
                start_vote($(this).data('pos'));
                return false;
            });
        }

        var $turn_info = $('.turn-info');
        var player_color_str = game_info.player_color == 1 ? "black" : "white";
        var your_turn_str = game_info.your_turn == 1 ? "" : "<b>not</b> ";
        var info_str = "You're " + player_color_str + '. ' +
            "It's " + your_turn_str + 'your turn.';

        $turn_info.html(info_str);
    }

    function redraw_votes_others(data) {
        var $votes_others = $('.congo-votes-others');
        $votes_others.empty();
        var votes = data['votes'];
        for(var i = 0; i < votes.length; i++) {
            var vote = votes[i];
            $votes_others.append($('<dt>' + vote.name + ' (' + vote.rating + ')</dt>'));
            $votes_others.append($('<dd>' + vote.notes + '</dd>'));
        }
    }

    function start_vote(pos) {
        if(! game_info.your_turn) {
            return false;
        }
        if(pos != 'tt') {
            var $sgf_cell = $('.sgf-cell-' + pos);

            if($sgf_cell.data('illegal')) {
                return false;
            }

            var $sgf_point = $sgf_cell.find('.sgf-point');

            if(!$sgf_point.hasClass('sgf-empty')) {
                return false;
            }
            $sgf_point.removeClass('sgf-empty');
            $sgf_point.addClass('sgf-vote');
        }
        else {
            $('.pass-button').addClass('pass-vote');
        }

        var y = pos.charCodeAt(0) - 97;

        if (y < 15) {
            $('.congo-vote-dialog').addClass('congo-vote-dialog-bottom');
        }
        else {
            $('.congo-vote-dialog').removeClass('congo-vote-dialog-bottom');
        }

        var $modal = $('#congo-vote-modal');

        $.getJSON('/api/game_votes/' + pos).done(function(data) {
            redraw_votes_others(data);
            $modal.modal('show');
            $modal.on('hide.bs.modal', function(event) {
                if(pos != 'tt') {
                    $sgf_point.removeClass('sgf-vote');
                    $sgf_point.addClass('sgf-empty');
                }
                else {
                    $('.pass-button').removeClass('pass-vote');
                }
            });
        }).error(function() {
            alert('Error.'); //TODO: make better;
        });

    }

    function sync_game() {
        $.getJSON('/api/game_state')
        .done(function(data) {
            gData = data;
            redraw_board(data);
            redraw_data_pane(data);
        });
    }

    r = redraw_board;

    sync_game();

});
