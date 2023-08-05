Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var chart_virtual = new Chart(document.getElementById("chart_virtual"), {
  type: 'doughnut',
  data: {
    labels: ["Used", "Free"],
    datasets: [{
      data: [],
      backgroundColor: ['#f6c23e', '#36b9cc'],
      hoverBackgroundColor: ['#f6c23e', '#36b9cc'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      callbacks: {
        label: function(tooltipItem) {
          return (chart_virtual.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] / 1024 / 1024 / 1024).toFixed(2) + ' GB';
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
    cutoutPercentage: 80
  },
});

function get_virtual() {
    $.ajax({url: "virtual", success: function(virtual) {
        virtual = JSON.parse(virtual)

        chart_virtual.data.datasets.forEach((dataset) => {
            dataset.data = [ virtual['used'], virtual['free']];
        });

        chart_virtual.update();
    }});
}

function refresh_virtual() {
    if (typeof get_virtual_interval !== 'undefined') {
        clearInterval(get_virtual_interval);
    }

    get_virtual_interval = setInterval(get_virtual, REFRESH_SECONDS * 1000);
}

get_virtual();
refresh_virtual();