$( document ).ready(function() {

    $('#success-alert').hide();

    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
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
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $( "#ask_for_permit" ).click(function() {
        var a=$('input:checked'); //выбираем все отмеченные checkbox
        var out=[]; //выходной массив

        for (var x=0; x<a.length;x++){ //перебераем все объекты
                out.push(a[x].value); //добавляем значения в выходной массив
                a[x].checked=false;
        }

        console.log(out);
        $.ajax({
            type: "POST",
            url: 'ask_for_permit/',
            data: {
                "contractor": $('#current_user').text(),
                "ids": out
            },
            success: function () {
                console.log('Success!');
                $('#success-alert').show();
                location.reload();
            }
        });
    });

    $(".close").click(function () {
        $('#success-alert').hide();
    });

    //
    console.log( "ready!" );
});



