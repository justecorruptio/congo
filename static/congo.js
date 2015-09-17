$(function() {

    $('#congo-signup-modal').on('shown.bs.modal', function () {
        $(this).find('input[name="name"]').focus()
    })

    $('#congo-login-modal').on('shown.bs.modal', function () {
        $(this).find('input[name="name"]').focus()
    })

    $("#congo-login-form").submit(function(event) {
        event.preventDefault();
        $.post(
            "/login",
            $(this).serialize()
        ).done(function(data) {
            window.location = '/';
        }).fail(function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        });
        return false;
    });

    $("#congo-signup-form").submit(function(event) {
        event.preventDefault();
        $.post(
            "/signup",
            $(this).serialize()
        ).done(function(data) {
            window.location = '/';
        }).fail(function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        });
        return false;
    });

    $('#congo-stats-modal').on('show.bs.modal', function () {
        $.getJSON("/stats").done(function(data) {
            $('.congo-num-players').text(data.num_players);
            $('.congo-num-votes').text(data.num_votes);

            $('.congo-white-team').html(data.white_players);
            $('.congo-black-team').html(data.black_players);

        }).fail(function() {
            alert('Failed to load stats.');
        });
    })

});
