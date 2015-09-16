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
                var pos = String.fromCharCode(97 + j, 97 + i);
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
                if(j == board_size - 1) {
                    $sgf_cell.append($('<div class=sgf-num-right num="' +
                        (board_size - i) + '"></div>'));
                }
                if(i == board_size - 1) {
                    $sgf_cell.append($('<div class=sgf-num-bottom num="' +
                        ("ABCDEFGHJKLMNOPQRST"[j]) + '"></div>'));
                }
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

        if (game_info.voted_move) {
            var $sgf_cell = $('.sgf-cell-' + game_info.voted_move);
            var $sgf_point = $sgf_cell.find('.sgf-point')
            $sgf_point.removeClass('sgf-empty');
            $sgf_point.addClass('sgf-voted');
        }

        var $board_info = $('.congo-board-info');
        $board_info.text(data['info']);
    }

    function redraw_data_pane(data) {

        if(game_info.current_seq != data.current_seq) {
            game_info.current_seq = data.current_seq;
            game_info.voted_move = null;
            game_info.your_turn = game_info.player_color % 2 == game_info.current_seq %2;
        }

        var $turn_info = $('.turn-info');
        var player_color_str = game_info.player_color == 1 ? "black" : "white";
        var your_turn_str
        if (game_info.voted_move) {
            your_turn_str = "You've voted.";
        }
        else {
            your_turn_str = "It's " +
                (game_info.your_turn == 1 ? "" : "<b>not</b> ") +
                'your turn.';
        }

        var info_str = "You're " + player_color_str + '. ' + your_turn_str;
        $turn_info.html(info_str);


        if(!game_info.your_turn) {
            return;
        }
        var board_votes = data['votes'];

        if(board_votes.length > 0) {
            $('.congo-top-votes-panel').show();
        }
        else{
            $('.congo-top-votes-panel').hide();
        }

        var $votes_table = $('.congo-votes-table');
        $votes_table.empty()

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

    }

    function redraw_votes_others(data) {
        var $votes_others = $('.congo-votes-others');
        $votes_others.empty();
        var votes = data['votes'];
        for(var i = 0; i < votes.length; i++) {
            var vote = votes[i];
            $votes_others.append($('<dt>' + vote.name + ' (' + vote.rating + ')</dt>'));
            var $dd = $('<dd></dd>');
            $dd.text(vote.notes);
            $votes_others.append($dd);
        }
        $('.congo-vote-count').text(data.count);
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

            if(
                !($sgf_point.hasClass('sgf-empty') ||
                $sgf_point.hasClass('sgf-voted'))
            ) {
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

        if( game_info.voted_move ) {
            $('.congo-cast-word').text('Update');
        }
        else {
            $('.congo-cast-word').text('Cast');
        }
        $('#congo-vote-form input[name="pos"]').val(pos);

        var $modal = $('#congo-vote-modal');

        $.getJSON('/api/game_votes/' + pos).done(function(data) {
            redraw_votes_others(data);
            stop_sync();
            $modal.modal('show');
            $modal.on('hide.bs.modal', function(event) {
                if(pos != 'tt') {
                    $sgf_point.removeClass('sgf-vote');
                    $sgf_point.addClass('sgf-empty');
                }
                else {
                    $('.pass-button').removeClass('pass-vote');
                }
                $('#congo-vote-form input[name="pos"]').val('');
                $('#congo-vote-form textarea[name="notes"]').val('');
                start_sync();
            });
        }).error(function() {
            alert('Error.'); //TODO: make better;
        });
    }

    $("#congo-vote-form").submit(function(event) {
        var pos = $('#congo-vote-form input[name="pos"]').val();
        event.preventDefault();
        $.post(
            "/api/vote",
            $(this).serialize()
        ).done(function(data) {
            var $modal = $('#congo-vote-modal');
            $modal.modal('hide');
            game_info.voted_move = pos;
            sync_game();
        }).fail(function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        });
        return false;
    });

    function sync_game() {
        $.getJSON('/api/game_state')
        .done(function(data) {
            redraw_data_pane(data);
            redraw_board(data);
        });
    }

    function start_sync() {
        if (sync_game_interval != 'stopped') {
            return;
        }
        sync_game_interval = window.setInterval(sync_game, 1 * 60 * 1000);
    }

    function stop_sync() {
        if (sync_game_interval == 'stopped') {
            return;
        }
        clearInterval(sync_game_interval);
        sync_game_interval = 'stopped';
    }

    sync_game_interval = 'stopped';
    start_sync();
    sync_game();

});
