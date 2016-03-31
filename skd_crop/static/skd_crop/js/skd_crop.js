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
        });
    });

    /* JCROP */
    var jcrop_api;
    var jcrop_data = {};

    $('#base_img').Jcrop({}, function(){
        jcrop_api = this;
    });

    $('.get_crop_size').click(function(){
        var crop_width = $(this).attr('data-crop-width');
        var crop_height = $(this).attr('data-crop-height');

        $('.get_crop_size').removeClass('active');
        $(this).addClass('active');

        jcrop_api.setSelect([ 0, 0, crop_width, crop_height ]);

        return false;
    });

    $('.get_crop_area').click(function(){
        var active_size = $('.get_crop_size.active').attr('data-crop-key');
        jcrop_data[active_size] = jcrop_api.tellSelect();
        $('.django_skd_crop-input').val(JSON.stringify(jcrop_data));
        return false;
    });

});
