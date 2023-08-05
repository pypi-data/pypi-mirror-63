// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

Chart.Legend.prototype.afterFit = function() {
    this.height = this.height + 20;
};

Chart.plugins.register({
   beforeDraw: function(c) {
      var legends = c.legend.legendItems;
      for (var i = 0; i < legends.length; i++) {
        legends[i].fillStyle = colors[i]
      }
   }
});

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

var chart_utilization = new Chart(document.getElementById("chart_utilization"), {
  type: 'line',
  data: {
    labels: [],
    datasets: [],
  },
  options: {
    animation: {
        easing: 'easeOutBack'
    },
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 0,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'time'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 12
        }
      }],
      yAxes: [{
        ticks: {
          suggestedMin: 0,
          suggestedMax: 100,
          maxTicksLimit: 10,
          padding: 10,
          callback: function(value, index, values) {
            return number_format(value) + '%';
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
      display: true,
      position: 'top',
      labels: {
        boxWidth: 30
      }
    }
  }
});

function get_utilization_chart() {
    $.ajax({url: "/performance/cpu/usage", success: function(load) {
        load = JSON.parse(load)['cpu'];

        var now = new Date();
        var hours = now.getHours() < 10 ? '0' + now.getHours() : now.getHours();
        var minutes = now.getMinutes() < 10 ? '0' + now.getMinutes() : now.getMinutes();
        var seconds = now.getSeconds() < 10 ? '0' + now.getSeconds() : now.getSeconds();

        chart_utilization.data.labels.shift();
        chart_utilization.data.datasets.forEach((dataset) => {
            dataset.data.shift();
        });
		
		chart_utilization.data.labels.push(hours + ':' + minutes + ':' + seconds);
        for (var i = 0; i < chart_utilization.data.datasets.length; i++) {
            chart_utilization.data.datasets[i].data.push(load[i])
        }

        chart_utilization.update();
    }});
}

colors = [];
for (var i = 0; i < 10; i++) {
    colors.push('#4e73df');
    colors.push('#1cc88a');
    colors.push('#f6c23e');
    colors.push('#e74a3b');
    colors.push('#36b9cc');
    colors.push('#858796');
}

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

$.ajax({url: "/performance/cpu/usage", success: function(load) {
    load = JSON.parse(load)['cpu'];
    for (var i = 0; i < load.length; i++) {
        color = hexToRgb(colors[i]);

        chart_utilization.data.datasets.push({
            label: "Core " + i,
            lineTension: 0.3,
            backgroundColor: "rgba(" + color.r + ", " + color.g + ", " + color.b + ", 0)",
            borderColor: "rgba(" + color.r + ", " + color.g + ", " + color.b + ", 1)",
            pointRadius: 0,
            pointHoverRadius: 0,
            pointHitRadius: 0,
            data: []
        });
    }

	for (var i = 0; i < 12; i++) {
		chart_utilization.data.labels.push('');
		for (var j = 0; j < chart_utilization.data.datasets.length; j++) {
		    chart_utilization.data.datasets[j].data.push(load[j])
		}
	}

    chart_utilization.update();
}});

function refresh_utilization_chart() {
    if (typeof get_utilization_chart_interval !== 'undefined') {
        clearInterval(get_utilization_chart_interval);
    }

    get_utilization_chart_interval = setInterval(get_utilization_chart, REFRESH_SECONDS * 1000);
}

get_utilization_chart();
refresh_utilization_chart();