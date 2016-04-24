var congo_bind_trial;

function insert_trial_tags($elem) {
    var html = $elem.html();
    var new_html = html.replace(
        /([A-Z]\d+( +[A-Z]\d+){2,30})/g,
        '<span class="congo-trial-span">$1</span>'
    );
    if (new_html != html) {
        $elem.html(new_html);
        congo_bind_trial($elem);
    }
}

$(function() {

    function redraw_board(data, skip_votes) {
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
                $sgf_cell.data('coord-i', i);
                $sgf_cell.data('coord-j', j);
                $sgf_cell.addClass('sgf-cell-' + pos);
                $sgf_cell.append($sgf_point);
                $sgf_cell.click(function(e) {
                    var pos = $(this).data('pos'),
                        i = $(this).data('coord-i'),
                        j = $(this).data('coord-j');
                    if (e.shiftKey) {
                        start_shift_click(board_size, i, j);
                        return false;
                    }
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

        var board_last_move = data['last_move'];
        var $sgf_cell = $('.sgf-cell-' + board_last_move);
        var $sgf_point = $sgf_cell.find('.sgf-point')
        $sgf_point.addClass('sgf-lastmove');

        var board_illegals = data['illegal'];
        for(var i = 0; i < board_illegals.length; i++) {
            var $sgf_cell = $('.sgf-cell-' + board_illegals[i]);
            $sgf_cell.data('illegal', true);
            var $sgf_point = $sgf_cell.find('.sgf-point')
            $sgf_point.attr('point-label', "\u25A2");
            $sgf_point.addClass('sgf-coord');
        }

        $('.congo-info-seq').text(data['seq']);
        $('.congo-info-turn').text(data['turn']);
        $('.congo-info-black-captures').text(data['black_captures']);
        $('.congo-info-white-captures').text(data['white_captures']);

        var board_marks = data['marks'] || [];
        for(var i = 0; i < board_marks.length; i++) {
            var mark = board_marks[i];
            var $sgf_cell = $('.sgf-cell-' + mark.pos);
            var $sgf_point = $sgf_cell.find('.sgf-point');
            $sgf_point.attr('point-label', mark.label);
            $sgf_point.addClass('sgf-coord');
        }

        if (!game_info.voted_move && !is_reviewing() || skip_votes) {
            // If you haven't voted, don't render votes.
            return;
        }

        var board_votes = data['votes'];
        for(var i = 0; i < board_votes.length; i++) {
            var vote = board_votes[i];
            var $sgf_cell = $('.sgf-cell-' + vote.pos);
            var $sgf_point = $sgf_cell.find('.sgf-point');
            $sgf_point.attr('point-label', vote.label)
            $sgf_point.addClass('sgf-coord');
        }

        var board_votes = data['comments'];
        for(var i = 0; i < board_votes.length; i++) {
            var vote = board_votes[i];
            var $sgf_cell = $('.sgf-cell-' + vote.pos);
            var $sgf_point = $sgf_cell.find('.sgf-point');
            if($sgf_point.hasClass('sgf-coord')) {
                continue;
            }
            $sgf_point.attr('point-label', '\u25B3')
            $sgf_point.addClass('sgf-coord');
        }

        if (game_info.voted_move && !is_reviewing()) {
            var $sgf_cell = $('.sgf-cell-' + game_info.voted_move);
            var $sgf_point = $sgf_cell.find('.sgf-point')
            $sgf_point.removeClass('sgf-empty');
            $sgf_point.addClass('sgf-voted');
        }

    }

    function redraw_data_pane(data) {

        if(game_info.current_seq != data.current_seq) {
            game_info.current_seq = data.current_seq;
            game_info.view_seq = data.current_seq;
            game_info.voted_move = null;
            game_info.your_turn = game_info.player_color % 2 == game_info.current_seq % 2;

        }

        var $turn_info = $('.turn-info');
        var player_color_str = game_info.player_color == 1 ? "black" : "white";
        var your_turn_str
        if (game_info.voted_move) {
            your_turn_str = "You've voted. ";
        }
        else {
            your_turn_str = "It's " +
                (game_info.your_turn == 1 ? "" : "<b>not</b> ") +
                'your turn. ';
        }

        var info_str = "You're " + player_color_str + '. ' + your_turn_str +
            "Turn ends in " + data['time_left'];
        $turn_info.html(info_str);


        var board_votes = data['votes'];

        if(board_votes.length > 0) {
            $('.congo-top-votes-panel').show();
        }
        else{
            $('.congo-top-votes-panel').hide();
        }

        if(!game_info.your_turn && !is_reviewing()) {
            return;
        }

        if(!game_info.voted_move && !is_reviewing()) {
            // If you haven't voted, don't render votes.
            $('.congo-votes-table').html(
                '<tr><td>Votes are hidden until you vote.</td></tr>'
            );
            return;
        }

        var $votes_table = $('.congo-votes-table');
        $votes_table.empty()

        for(var i = 0; i < board_votes.length && i < 3; i++) {
            var vote = board_votes[i];
            var $tr = $('<tr>' +
                '<td><a href="" data-pos="' + vote.pos + '"' +
                ' class="data-pane-label">' + vote.label + '</a></td>' +
                '<td>' + vote.count + ' votes</td>' +
            '</tr>');
            $votes_table.append($tr);

            $('.data-pane-label').unbind("click");
            $('.data-pane-label').click(function(event) {
                event.preventDefault();
                start_vote($(this).data('pos'));
                return false;
            });
        }
    }

    function redraw_system_message(data) {
        var message = data['system_message'];
        if(message) {
            $('.congo-system-message').html(message);
            $('.congo-system-message-panel').show();
        }
        else {
            $('.congo-system-message-panel').hide();
        }
    }

    function redraw_votes_others(data) {
        var $votes_others = $('.congo-votes-others');
        $votes_others.empty();
        var votes = data['votes'];
        for(var i = 0; i < votes.length; i++) {
            var vote = votes[i];
            $votes_others.append($(
                '<dt>' + vote.name + ' (' + vote.rating + ') ' +
                '<small class="congo-note-type">' + vote.type + '</small>' + '</dt>'
            ));
            var $dd = $('<dd></dd>');
            $dd.text(vote.notes);
            insert_trial_tags($dd);
            $votes_others.append($dd);
        }
        $('.congo-vote-count').text(data.count);
    }

    function start_vote(pos) {
        if(!game_info.your_turn && !is_reviewing()) {
            return false;
        }

        if(game_info.voted_move) {
            $('.congo-comment-button').show();
        }
        else {
            $('.congo-comment-button').hide();
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

        if(!is_reviewing()) {
            if( game_info.voted_move ) {
                $('.congo-vote-title').text('Update Vote');
            }
            else {
                $('.congo-vote-title').text('Cast Vote');
            }
        }
        else {
            $('.congo-vote-title').text('Reviewing Vote');
        }

        $('#congo-vote-form input[name="pos"]').val(pos);

        var $modal = $('#congo-vote-modal');

        $.getJSON('/api/game_votes/' + game_info.view_seq + '/' + pos).done(function(data) {
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
                if(!is_reviewing()) {
                    start_sync();
                }
            });
        }).error(function() {
            alert('Error.'); //TODO: make better;
        });
    }

    var trial_data = 0;
    function start_shift_click(board_size, i, j) {
        var pretty_pos = "ABCDEFGHJKLMNOPQRST"[j] + (board_size - i);
        var $chat_input = $('#congo-chat-input');
        var chat_val = $chat_input.val();

        if (!trial_data) {
            trial_data = $.parseJSON(last_synced_data);
            chat_val = chat_val.replace(/( *[A-Z]\d+)*/g,'');
        }

        var valid_move = play_move(
            trial_data['board'],
            2 - trial_data['seq'] % 2,
            [i, j]
        );

        if (valid_move) {
            trial_data['seq'] += 1;
            redraw_board(trial_data, true);
            $chat_input.val(chat_val + ' ' + pretty_pos);
        }

        $(document).unbind("keyup");
        $(document).keyup(function(e) {
            redraw_board($.parseJSON(last_synced_data));
            trial_data = 0;
            $(this).unbind(e);
        });
    }

    $("#congo-vote-form").submit(function(event) {
        var $notes = $('#congo-vote-form textarea[name="notes"]');
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

    $(".congo-comment-button").click(function(event) {
        var $notes = $('#congo-vote-form textarea[name="notes"]');
        var pos = $('#congo-vote-form input[name="pos"]').val();
        if($notes.val().length < 1) {
            alert("Comments cannot be empty.");
            return false;
        }
        event.preventDefault();
        $.post(
            "/api/comment",
            $("#congo-vote-form").serialize()
        ).done(function(data) {
            var $modal = $('#congo-vote-modal');
            $modal.modal('hide');
            sync_game();
        }).fail(function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        });
        return false;
    });

    $(".review-backward-button").click(function(event) {
        event.preventDefault();
        if(game_info.view_seq == 1) {
            this.blur();
            return false;
        }
        game_info.view_seq -= 1;
        $(".review-forward-button").removeClass("text-muted");
        if(game_info.view_seq == 1) {
            $(".review-backward-button").addClass("text-muted");
        }
        $('.congo-vote-form-pane').hide();
        stop_sync();
        sync_game();
        this.blur();
        return false;
    });

    $(".review-forward-button").click(function(event) {
        event.preventDefault();
        if(!is_reviewing()) {
            this.blur();
            return false;
        }
        game_info.view_seq += 1;
        $(".review-backward-button").removeClass("text-muted");
        if(!is_reviewing()) {
            $(".review-forward-button").addClass("text-muted");
            $('.congo-vote-form-pane').show();
            start_sync();
        }
        sync_game();
        this.blur();
        return false;
    });

    var last_synced_data;
    function sync_game() {
        $.getJSON('/api/game_state/' + game_info.view_seq)
        .done(function(data) {
            last_synced_data = JSON.stringify(data);

            redraw_data_pane(data);
            redraw_board(data);
            redraw_system_message(data);
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

    function is_reviewing() {
        return game_info.view_seq != game_info.current_seq;
    }

    sync_game_interval = 'stopped';
    start_sync();
    sync_game();

    congo_bind_trial = function($elem) {
        $elem.find('.congo-trial-span').unbind('mousedown touchstart');
        $elem.find('.congo-trial-span').bind('mousedown touchstart', function(e) {
            var text = $.trim($(this).text());
            var moves = text.split(/ +/).map(human_coord_to_pos);
            var trial_data = $.parseJSON(last_synced_data);
            trial_data['marks'] = [];
            for(var x = 0; x < moves.length; x ++) {
                play_move(trial_data['board'], 2 - trial_data['seq'] % 2, moves[x]);
                trial_data['marks'].push({
                    'pos': pos_to_sgf(moves[x]),
                    'label': '' + (x + 1)
                });
                trial_data['seq'] += 1;
            }
            redraw_board(trial_data, true);
            $('.modal').addClass('invis-trial-xs');
        });
        $elem.find('.congo-trial-span').unbind('mouseup touchend');
        $elem.find('.congo-trial-span').bind('mouseup touchend', function(e) {
            $('.modal').removeClass('invis-trial-xs');
            redraw_board($.parseJSON(last_synced_data));
        });
    };
});
