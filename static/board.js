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

        var board_votes = data['votes'];
        for(var i = 0; i < board_votes.length; i++) {
            var vote = board_votes[i];
            var $tr = $('<tr>' +
                '<td><a>' + vote.label + '</a></td>' +
                '<td>' + vote.count + ' votes</td>' +
            '</tr>');
            $votes_table.append($tr);
        }

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
