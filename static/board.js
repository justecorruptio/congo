$(function() {

    function redraw_board(data) {
        console.debug("YO!");
        var $sgf_board = $('.sgf-board');
        var board_size = data['board_size'];
        var board_data = data['board'];
        for(var i = 0; i < board_size; i++) {
            var $sgf_row = $('<div class="sgf-row"></div>');
            for(var j = 0; j < board_size; j++) {
                var $sgf_point = $('<div class="sgf-point"></div>');
                var color = board_data[i][j];
                $sgf_point.addClass({
                    0: 'sgf-empty',
                    1: 'sgf-black',
                    2: 'sgf-white'
                }[color]);
                var $sgf_cell = $('<div class="sgf-cell"></div>');
                $sgf_cell.append($sgf_point);
                $sgf_row.append($sgf_cell);
            }
            $sgf_board.append($sgf_row);
        }
    }

    function sync_game() {
        $.getJSON('/api/game_state')
        .done(function(data) {
            redraw_board(data);
        });
    }

    sync_game();

});
