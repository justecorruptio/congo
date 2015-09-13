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

});
