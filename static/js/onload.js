$(function () {

    $("#submit").on("click", function () { ajax_send(); });

});

function ajax_send() {

    var user_param = { comment: $("#comment").val() };

    $.ajax({
        url: "",
        contentType: 'application/json; charset=utf-8',
        type: "POST",
        data: JSON.stringify(user_param),
    }).done(function (data, status, xhr) {
        $("#comment_area").html(data.content);
    }).fail(function (xhr, status, error) {
        console.log(status + ":" + error);
    });

}