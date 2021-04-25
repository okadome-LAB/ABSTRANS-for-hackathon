function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

/*jQuery起動テスト用*/
jQuery(function () {
    jQuery('#test').text('hello_jQuery!');
});
/*------------------*/


/*ajaxテスト用*/
$(document).ready(function () {
    $('#activate').click(function (event) {
        var test_value = $('#activate').val();
        alert(test_value + '_is_requested')
        event.preventDefault();
        $.ajax({
            url: "/activate_ajax/",
            type: "POST",
            dataType: "json",
            //contentType: "application/json; charset=utf-8",
            contentType: "application/x-www-form-urlencoded",
            data: {
                'test_value': test_value,
            },
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function (data) {
                console.log(data);
                $('#embed').text(data)
                alert(data)
            },
            error: function (req, text) {
                console.log(text);
            },
        });
    });
});