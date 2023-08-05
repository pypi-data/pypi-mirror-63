Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
const TABLE_PAGE_LENGTH = 4

var table_partitions = $('#table_partitions').DataTable({
    'searching': false,
    'info': false,
    'lengthChange': false,
    'pageLength': TABLE_PAGE_LENGTH,
    'ordering': false
});

$('#table_partitions tbody').on('click', 'tr', function () {
    table_partitions.$('tr.selected').removeClass('selected');
    $(this).addClass('selected');

    if (table_partitions.row(this).data()[2] && table_partitions.row(this).data()[2] != '&nbsp;') {
        get_information(table_partitions.row(this).data()[1])
    }
});

var chart_usage = new Chart(document.getElementById("chart_usage"), {
  type: 'doughnut',
  data: {
    labels: ["Used", "Free"],
    datasets: [{
      data: [],
      backgroundColor: ['#e74a3b', '#1cc88a'],
      hoverBackgroundColor: ['#e74a3b', '#1cc88a'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      callbacks: {
        label: function(tooltipItem) {
          var gigabytes = chart_usage.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] / 1024 / 1024 / 1024;
          return gigabytes >= 1024 ? (gigabytes / 1024).toFixed(2) + ' TB' : gigabytes.toFixed(2) + ' GB';
        }
      },
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});

function get_information(device) {
    $.ajax({url: "usage/" + device, success: function(usage) {
        usage = JSON.parse(usage);

        $("#device").text(device);

        total_gigabytes = usage['total'] / 1024 / 1024 / 1024;
        used_gigabytes = usage['used'] / 1024 / 1024 / 1024;
        free_gigabytes = usage['free'] / 1024 / 1024 / 1024;

        if (total_gigabytes >= 1024) {
            $("#total").text('Total memory: ' + (total_gigabytes / 1024).toFixed(2) + ' TB');
        } else {
            $("#total").text('Total memory: ' + total_gigabytes.toFixed(2) + ' GB');
        }

        if (used_gigabytes >= 1024) {
            $("#used").text('Used: ' + (used_gigabytes / 1024).toFixed(2) + ' TB');
        } else {
            $("#used").text('Used: ' + used_gigabytes.toFixed(2) + ' GB');
        }

        if (free_gigabytes >= 1024) {
            $("#free").text('Free: ' + (free_gigabytes / 1024).toFixed(2) + ' TB');
        } else {
            $("#free").text('Free: ' + free_gigabytes.toFixed(2) + ' GB');
        }

        chart_usage.data.datasets.forEach((dataset) => {
            dataset.data = [usage['used'], usage['free']];
        });

        chart_usage.update();
    }});
}

$.ajax({url: "partitions", success: function(partitions) {
    partitions = JSON.parse(partitions)['partitions']

    for (var i = 0; i < partitions.length; i++) {
        partition = partitions[i]

        device = partition[0];
        mountpoint = partition[1];
        filesystem = partition[2];
        options = partition[3];

        table_partitions.row.add([device, mountpoint, filesystem, options]).draw();
    }

    for (var i = 0; i < TABLE_PAGE_LENGTH - partitions.length; i++) {
        table_partitions.row.add(['&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;']).draw();
    }

    $(table_partitions.row(0).node()).addClass('selected');
    get_information(partitions[0][1])
}});
