Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };

  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

var chart_times = new Chart(document.getElementById("chart_times"), {
    type: 'doughnut',
    data: {
      labels: ["User", "System", "Idle"],
      datasets: [{
        data: [],
        backgroundColor: ['#4e73df', '#f6c23e', '#1cc88a'],
        hoverBackgroundColor: ['#4e73df', '#f6c23e', '#1cc88a'],
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        callbacks: {
            label: function(tooltipItem) {
                return number_format(chart_times.data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]);
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

function get_times() {
    $.ajax({url: "times", success: function(times) {
        times = JSON.parse(times)

        chart_times.data.datasets.forEach((dataset) => {
            dataset.data = [times['user'], times['system'], times['idle']];
        });

        chart_times.update();
    }});
}

function refresh_times() {
    if (typeof get_times_interval !== 'undefined') {
        clearInterval(get_times_interval);
    }

    get_times_interval = setInterval(get_times, REFRESH_SECONDS * 1000);
}

get_times();
refresh_times();