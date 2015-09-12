$(function() {

    $('#congo-signup-modal').on('shown.bs.modal', function () {
        $('#name').focus()
    })

    $("#congo-signup-form").submit(function(event) {
        event.preventDefault();
        $.post(
            "/signup",
            $(this).serialize()
        ).done(function(data) {
            alert(data);
        }).fail(function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseText);
        });
        return false;
    });

});
