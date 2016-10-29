$(function () {
    var charts = $('#container').highcharts({
        chart: {
            type: 'area'
        },
        title: {
            text: null
        },

        xAxis: {
            categories: []
        },
        yAxis: {
            //gridLineWidth: 0,
            title: {
                text: null
            },
            labels:{
                enabled:false
            }
        },
        legend: {
            enabled:false
        },
        credits: {
            enabled: false
        },
        tooltip: {
            formatter: function () {
                return  this.x +':'+ this.y

            }
        },
        plotOptions: {

        },
        series: [{
            name: null,
            data: []
        }]
    });
});