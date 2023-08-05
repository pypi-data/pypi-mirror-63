Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var chart_swap = new Chart(document.getElementById("chart_swap"), {
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
          return (chart_swap.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] / 1024 / 1024 / 1024).toFixed(2) + ' GB';
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

function get_swap() {
    $.ajax({url: "swap", success: function(swap) {
        swap = JSON.parse(swap)

        chart_swap.data.datasets.forEach((dataset) => {
            dataset.data = [swap['used'], swap['free']];
        });

        chart_swap.update();
    }});
}

function refresh_swap() {
    if (typeof get_swap_interval !== 'undefined') {
        clearInterval(get_swap_interval);
    }

    get_swap_interval = setInterval(get_swap, REFRESH_SECONDS * 1000);
}

get_swap();
refresh_swap();