function get_utilization() {
    $.ajax({url: "utilization", success: function(utilization) {
        utilization = JSON.parse(utilization);
        $("#utilization").css("width", utilization['cpu'] + '%');
    }});
}

function refresh_utilization() {
    if (typeof get_utilization_interval !== 'undefined') {
        clearInterval(get_utilization_interval);
    }

    get_utilization_interval = setInterval(get_utilization, REFRESH_SECONDS * 1000);
}

get_utilization();
refresh_utilization();