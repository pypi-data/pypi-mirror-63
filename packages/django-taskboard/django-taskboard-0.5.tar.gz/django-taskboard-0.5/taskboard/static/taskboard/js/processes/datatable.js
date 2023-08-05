table_all = $('#dataTable').DataTable({
    'scrollX': true,
    ajax: { url: 'all' },
    columns: [
        { data: 'name' },
        { data: 'pid' },
        { data: 'username' },
        { data: 'exe' },
        {
            'width': '10%',
            'render': function(data, type, row, meta) {
                return row.cpu + '%';
            }
        },
        {
            'width': '10%',
            'render': function(data, type, row, meta) {
                return row.memory + '%';
            }
        },
        {
            'orderable': false,
            'width': '5%',
            'render': function(data, type, row, meta) {
                return '<center><a data-toggle="modal" data-target="#stopProcessModal" data-name="' + row.name + '" data-pid="'+ row.pid +'" data-index="' + meta.row + '" style="cursor: pointer;"><i class="fas fa-times"></i></a></center>';
            }
        }
    ]
});

function get_all_processes() {
    table_all.ajax.reload(null, false);
}

function refresh_all_processes() {
    if (typeof get_all_processes_interval !== 'undefined') {
        clearInterval(get_all_processes_interval);
    }

    get_all_processes_interval = setInterval(get_all_processes, REFRESH_SECONDS * 1000);
}

get_all_processes();
refresh_all_processes();