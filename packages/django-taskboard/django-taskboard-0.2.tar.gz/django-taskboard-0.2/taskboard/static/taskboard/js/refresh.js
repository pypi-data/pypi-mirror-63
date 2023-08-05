var REFRESH_SECONDS = sessionStorage.getItem('refresh') > 0 ? sessionStorage.getItem('refresh') : 5;
$("#refresh_" + REFRESH_SECONDS).addClass('current');

function select_refresh(page, seconds) {
    $("#refresh_" + REFRESH_SECONDS).removeClass('current');

    REFRESH_SECONDS = seconds;
    sessionStorage.setItem('refresh', REFRESH_SECONDS)
    $("#refresh_" + REFRESH_SECONDS).addClass('current');

    switch(page) {
        case 'CPU': refresh_cpu(); break;
        case 'Memory': refresh_memory(); break;
        case 'Disk': refresh_disk(); break;
        case 'Network': refresh_network(); break;
        case 'Processes': refresh_processes(); break;
    }
}

function refresh_cpu() {
    refresh_statistics();
    refresh_times();
    refresh_utilization();
    refresh_utilization_chart();
}

function refresh_memory() {
    refresh_information();
    refresh_virtual();
    refresh_swap();
}

function refresh_disk() {
    refresh_io_counters_chart();
}

function refresh_network() {
}

function refresh_processes() {
    refresh_all_processes();
}