$(function () {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    $('input:file').on('change', function (e) {
        var file_input = $(this);
        var image = file_input[0];
        var img_id = '#img_' + image.name;
        var data = new FormData();
        data.append('image', image.files[0]);
        data.append('upload_to', file_input.attr('data-upload-to'));
        data.append('resize_source', file_input.attr('data-resize-source'));
        $.ajax({
            url: '/skd-crop/upload/',
            data: data,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function (data) {
                $(img_id).attr('src', data.url);
            }
        })

    })
});
