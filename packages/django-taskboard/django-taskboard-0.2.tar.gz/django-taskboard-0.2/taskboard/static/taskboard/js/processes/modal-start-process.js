$('#startProcess').on('click', function(e) {
    var executablePath = $('#executablePath').val();
    var executableArgs = $('#executableArgs').val();

    if (executablePath) {
        startProcess(executablePath, executableArgs);
    } else {
        // No input
    }
});

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

function startProcess(path, args) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

    $.ajax({
        url: '/system/processes/start/',
        type: 'POST',
        data: {
            'path': path,
            'args': args
        },
        success: function(success) {
            success = JSON.parse(success)['success']

            if (success) {
                $('#startProcessModal').modal('toggle');
                $('#executablePath').val('');
                $('#executableArgs').val('');
            }
    }});
}