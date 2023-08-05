$('#stopProcessModal').on('show.bs.modal', function(e) {
    var name = $(e.relatedTarget).data('name');
    var pid = $(e.relatedTarget).data('pid');
    var index = $(e.relatedTarget).data('index');

    $('#processName').text('Stop process "' + name + '"?')
    $('#stopProcess').attr('onclick', 'stopProcess(' + pid + ', ' + index + ')')
});

function stopProcess(pid, index) {
    $.ajax({url: "/system/processes/stop/" + pid, success: function(success) {
        success = JSON.parse(success)['success']
        $('#stopProcessModal').modal('toggle');

        if (success) {
            table_all.row(index).remove().draw();
        }
    }});
}