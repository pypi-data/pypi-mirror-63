function get_information() {
    $.ajax({url: "virtual", success: function(virtual) {
        $.ajax({url: "swap", success: function(swap) {
            virtual = JSON.parse(virtual)
            swap = JSON.parse(swap)

            $("#total_virtual").text('Total memory: ' + (virtual['total'] / 1024 / 1024 / 1024).toFixed(2) + ' GB');
            $("#used_virtual").text('Used: ' + (virtual['used'] / 1024 / 1024 / 1024).toFixed(2) + ' GB');
            $("#free_virtual").text('Free: ' + (virtual['free'] / 1024 / 1024 / 1024).toFixed(2) + ' GB');

            $("#total_swap").text('Total memory: ' + (swap['total'] / 1024 / 1024 / 1024).toFixed(2) + ' GB');
            $("#used_swap").text('Used: ' + (swap['used'] / 1024 / 1024 / 1024).toFixed(2) + ' GB');
            $("#free_swap").text('Free: ' + (swap['free'] / 1024 / 1024 / 1024).toFixed(2) + ' GB');
        }});
    }});
}

function refresh_information() {
    if (typeof get_information_interval !== 'undefined') {
        clearInterval(get_information_interval);
    }

    get_information_interval = setInterval(get_information, REFRESH_SECONDS * 1000);
}

get_information();
refresh_information();