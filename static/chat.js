$(function() {

    function insert_trial_tags($elem) {
        var html = $elem.html();
        var new_html = html.replace(
            /([A-Z]\d+( +[A-Z]\d+){1,100})/g,
            '<span class="congo-trial-span">$1</span>'
        );
        if (new_html != html) {
            $elem.html(new_html);
            congo_bind_trial($elem);
        }
    }

    function time() {
        return new Date().getTime() / 1000.;
    }

    function name_to_color(name) {
        var rgb = [0, 0, 0];
        for(var i = 0; i < name.length; i ++) {
            rgb[i % 3] = (rgb[i % 3] + name.charCodeAt(i)) % (i == 1? 4 : 3);
        }
        var r = rgb[0] * 35 + 50;
        var g = rgb[1] * 35 + 50;
        var b = rgb[2] * 35 + 50;
        return 'rgb(' + r + ',' + g + ',' + b + ')';
    }

    function name_to_color(name) {
        var h = 0
        for(var i = 0; i < name.length; i ++) {
            h += name.charCodeAt(i);
        }
        h = (h % 12) * 30;
        return 'hsl(' + h + ', 30%, 50%)';
    }

    $('#congo-chat-modal').on('shown.bs.modal', function () {
        var $chat_container = $('#congo-chat-container');
        $(".congo-chat-modal-body").append($chat_container);
        var $chat_body = $('.chat-body');
        $chat_body.scrollTop($chat_body.prop('scrollHeight'));
    });

    $('#congo-chat-modal').on('hidden.bs.modal', function () {
        var $chat_container = $('#congo-chat-container');
        $(".congo-chat-panel").append($chat_container);
    });

    function poll_chat() {
        if(chat_xhr) {
            return false;
        }

        chat_xhr = $.getJSON('/chat?last_id=' + chat_last_id).done(function(data) {
            chat_xhr = false;
            var $chat_body = $('.chat-body');
            if(data.refresh) {
                $chat_body.html('');
            }
            if(data.messages.length != 0) {
                for(var i = 0; i < data.messages.length; i ++) {
                    var msg = data.messages[i];
                    var delete_button = msg.deletable ?
                        '<a class="chat-delete" data-chat_id="' + msg.id + '" href="">X </a>'
                        :'';


                    var $line_span = $(
                        '<div class="chat-line" data-chat_id="' + msg.id + '">' +
                            '<b><span class="chat-name"></span></b>: ' +
                            delete_button +
                            '<span class="chat-message"></span>' +
                        '</div>'
                    );
                    if(msg.name) {
                        $line_span.find('.chat-name').text(msg.name + ' (' + msg.rating + ')');
                        $line_span.find('.chat-name').css('color', name_to_color(msg.name));
                    }
                    else {
                        $line_span.find('.chat-name').text('ConGo Bot');
                        $line_span.find('.chat-message').css('font-weight', 'bold');
                    }
                    $line_span.find('.chat-message').text(msg.message);
                    insert_trial_tags($line_span.find('.chat-message'));

                    $chat_body.append($line_span);
                    chat_last_id = msg.id;
                }
                while ($chat_body.find('.chat-line').length > 1000) {
                    $chat_body.find('.chat-line:first').remove();
                }
                $chat_body.scrollTop($chat_body.prop('scrollHeight'));
            }

            if(data.delete_id) {
                $('.chat-line[data-chat_id="' + data.delete_id + '"]').remove();
            }

            $('.chat-delete').unbind("click");
            $('.chat-delete').click(function(event) {
                event.preventDefault();
                $.ajax({
                    url: '/chat?id=' + $(this).data('chat_id'),
                    type: 'DELETE'
                });
                return false;
            });

            var online_users = data['online_users'];
            var num_online = online_users.length;
            $('.chat-whois-online').html('Currently: <b>' + num_online + '</b> user' +
                (num_online != 1? 's': '') + ' online');

            whois_data = '';
            for(var i = 0; i < online_users.length; i ++) {
                whois_data += '<b>' + online_users[i].name + ' (' +
                    online_users[i].rating + ')<br/>';
            }

            $('.congo-whois-online-pane').html(whois_data);

            poll_chat();

        }).fail(function () {
            chat_xhr = false;
            chat_last_id = 0;
            var $chat_body = $('.chat-body');
            $chat_body.append(
                '<div class="chat-line">' +
                    '<span class="chat-reconnect btn btn-warning btn-sm">' +
                        'Disconnected, click to reconnect.' +
                    '</span>' +
                '</div>'
            );

            $('.chat-reconnect').click(function() {
                var $chat_body = $('.chat-body');
                $chat_body.html('');
                poll_chat();
            });

            $chat_body.scrollTop($chat_body.prop('scrollHeight'));
        });
    };

    $("#congo-chat-form").submit(function(event) {
        event.preventDefault();
        var $chat_input = $('#congo-chat-form input[name="message"]');
        if(time() - last_chat_ts < 1) {
            alert("Please slow down.");
            return false;
        }
        if($chat_input.val().length < 1) {
            alert("Please enter a message.");
            return false;
        }
        $.post(
            "/chat",
            $(this).serialize()
        ).done(function(data) {
            $chat_input.val('');
            last_chat_ts = time();
        }).fail(function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        });
        return false;
    });

    chat_xhr = false;
    chat_last_id = 0;
    last_chat_ts = 0;
    poll_chat();

});
