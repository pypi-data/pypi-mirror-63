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

var chart_io_counters_count = new Chart(document.getElementById("chart_io_counters_count"), {
  type: 'bar',
  data: {
    labels: ["Read count", "Write count"],
    datasets: [{
      backgroundColor: "#4e73df",
      hoverBackgroundColor: "#2e59d9",
      borderColor: "#4e73df",
      data: [],
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 2
        },
        maxBarThickness: 100,
      }],
      yAxes: [{
        ticks: {
          min: 0,
          maxTicksLimit: 10,
          padding: 10,
          callback: function(value) {
            return number_format(value);
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          return number_format(tooltipItem.yLabel);
        }
      }
    },
  }
});

var chart_io_counters_bytes = new Chart(document.getElementById("chart_io_counters_bytes"), {
  type: 'bar',
  data: {
    labels: ["Read bytes", "Write bytes"],
    datasets: [{
      backgroundColor: "#4e73df",
      hoverBackgroundColor: "#2e59d9",
      borderColor: "#4e73df",
      data: [],
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 2
        },
        maxBarThickness: 100,
      }],
      yAxes: [{
        ticks: {
          min: 0,
          maxTicksLimit: 10,
          padding: 10,
          callback: function(value) {
            return number_format(value);
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          return number_format(tooltipItem.yLabel);
        }
      }
    },
  }
});

function get_io_counters() {
  $.ajax({url: "io_counters", success: function(io_counters) {
    io_counters = JSON.parse(io_counters);

    chart_io_counters_count.data.datasets.forEach((dataset) => {
      dataset.data = [io_counters['read_count'], io_counters['write_count']];
    });

    chart_io_counters_bytes.data.datasets.forEach((dataset) => {
      dataset.data = [io_counters['read_bytes'], io_counters['write_bytes']];
    });

    chart_io_counters_count.update();
    chart_io_counters_bytes.update();
  }});
}

function refresh_io_counters_chart() {
    if (typeof get_io_counters_interval !== 'undefined') {
        clearInterval(get_io_counters_interval);
    }

    get_io_counters_interval = setInterval(get_io_counters, REFRESH_SECONDS * 1000);
}

get_io_counters();
refresh_io_counters_chart();