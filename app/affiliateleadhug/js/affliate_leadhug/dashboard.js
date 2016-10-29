var dashboard = avalon.define(
    {
        $id:'dashboard',
        paid:{
            today:'',
            balance:'',
            total_paid:'',
        },
        account_manager:{
        },
        clicks_conversions:{
            'clicks':'',
            'conversions':''
        },
        high_income_offers:[],
        lastest_offers:[],
        featured_offers:[],
        status:'',
        get_data:function(func){
            var url = '/highcharts/data?time='+'today';
            $.getJSON(url, {}, function(o) {
                 if (!o.err) {
                    func(o)
                    console.log(o)
                }
            });

        }
    }
)

avalon.ready(
    function(){
        avalon.vmodels.dashboard.get_data(function(data){
        $('#container').highcharts({
        title: {
            text: 'Click & Conversion Stastics',
            x: -20 //center
        },
        subtitle: {
            text: '',
            x: -20
        },
        xAxis: {
            categories: data.clicks.x
        },
        yAxis: {
            title: {
                text: ''
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: ''
        },
        credits:{
            enabled:false
        },
        exporting: {
            enabled:true,
            buttons: {
                contextButton: {
                    menuItems: [{
                        text: 'today',
                        onclick: function () {
                            var url = '/highcharts/data?time='+'today';
                            $.getJSON(url, {}, function(o) {
                                if (!o.err) {
                                    var chart = $('#container').highcharts();
                                        chart.series[0].setData(o.clicks.y)
                                        chart.series[1].setData(o.conversions.y)
                                        chart.xAxis[0].setCategories(o.clicks.x);

                                }
                            });
                        },
                    }, {
                        text: 'last 7 days',
                        onclick: function () {
                            var url = '/highcharts/data?time='+'7days';
                            $.getJSON(url, {}, function(o) {
                                if (!o.err) {
                                      var chart = $('#container').highcharts();
                                        chart.series[0].setData(o.clicks.y);
                                        chart.series[1].setData(o.conversions.y);
                                        chart.xAxis[0].setCategories(o.clicks.x);
                                }
                            });
                        },
                        separator: false
                    }, {
                        text: 'last 14 days',
                        onclick: function () {
                            var url = '/highcharts/data?time='+'14days';
                            $.getJSON(url, {}, function(o) {
                                if (!o.err) {
                                       var chart = $('#container').highcharts();
                                        chart.series[0].setData(o.clicks.y);
                                        chart.series[1].setData(o.conversions.y);
                                        chart.xAxis[0].setCategories(o.clicks.x);
                                }
                            });
                        },
                        separator: false
                    },{
                        text: 'last 8 weeks',
                        onclick: function () {
                            var url = '/highcharts/data?time='+'8weeks';
                            $.getJSON(url, {}, function(o) {
                                if (!o.err) {
                                      var chart = $('#container').highcharts();
                                        chart.series[0].setData(o.clicks.y);
                                        chart.series[1].setData(o.conversions.y);
                                        chart.xAxis[0].setCategories(o.clicks.x);
                                }
                            });
                        },
                        separator: false
                    }
                    ]
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'click',
            data: data.clicks.y
        },{
            name: 'conversion',
            data: data.conversions.y
        },
        ]
    });
        }
        );
    }
)
