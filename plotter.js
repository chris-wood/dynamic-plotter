function readFromFile(series, filename) {
    var debug = false;
    if (debug) {
        return ["" + Math.random()];
    } else {
        var file = new File([""], filename, {type: "text/plain"});
        var reader = new FileReader();
        reader.onload = function(e) {
            var lines = e.target.result;
            console.log(e.target);
            var x = (new Date()).getTime();
            var y = parseInt(lines[lines.length - 1]);

            console.log([x, y]);

            series.addPoint([x, y,], true, true);
        };
        // console.log(file);
        reader.readAsText(file);
    }
}

// Look for new files that match the schema

$(function () {
    $(document).ready(function () {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

        $('#container').highcharts({
            chart: {
                type: 'spline',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function () {

                        // set up the updating of the chart each second
                        var series = this.series[0];
                        setInterval(function() {
                            readFromFile(series, "out.csv");
                        }, 500);
                    }
                }
            },
            title: {
                text: 'CCNx Tutorial Attendee Data'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Value'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'Wireless Signal',
                data: (function () {
                    var data = [];
                    var time = (new Date()).getTime();
                    var numSeconds = 20;

                    for (var i = numSeconds * -1; i <= 0; i += 1) {
                        data.push({
                            x: time + i * 1000,
                            y: Math.random()
                        });
                    }
                    return data;
                }())
            }]
        });
    });
});
