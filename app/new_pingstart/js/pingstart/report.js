var pingstart = Pingstart;
var Report;
Report = avalon.define({
    $id: 'report',
    slots: [
        {
            _id: '',
            name: ''
        }
    ],

    overview: {
        overview_ps_data: {
            revenue: '',
            CPC: '',
            ECPM: ''
        },
        overview_total_data: {
            revenue: '',
            CPC: '',
            ECPM: ''
        }
    },

    start: pingstart.getBeforeDate(7),
    end: pingstart.getBeforeDate(1),

    slot: '',

    date_or_country: 'date',
    network_detail_data:[],
    table:[{}],
    total:{},
    foot:{},
    table_data: [
        {
            createdTime: '',
            show_revenue: '',
            show_click: '',
            impression: '',
            CPC: '',
            fill: '',
            request: '',
            eCPM: '',
            CTR: '',
            FillRate: ''
        }
    ],

    total_datas: {
        show_revenue: '',
        show_click: '',
        impression: '',
        CPC: '',
        fill: '',
        request: '',
        eCPM: '',
        CTR: '',
        FillRate: ''
    },

    foot_total_datas: {
        show_revenue: '',
        show_click: '',
        impression: '',
        CPC: '',
        fill: '',
        request: '',
        eCPM: '',
        CTR: '',
        FillRate: ''
    },

    get_report_stats: function(){
        $("#btn-box li span").removeClass("btn_bg_color");
        $("#show_revenue").addClass("btn_bg_color");
        $('#container, #btn-box').show();
        Report.date_or_country = 'date'
        var data = {
            start: Report.start,
            end: Report.end,
            slot: Report.slot,
            date_or_country: 'date'
        }
       $.blockUI({
            css : {
                top: '400px'
            }
        })
        $.postJSON1("/report/stats", data, function (o) {
            if(!o.err){
                Report.network_detail_data = o.network_detail_data;
                Report.table_data = o.table_data;
                Report.total_datas = o.total_datas;
                Report.foot_total_datas = o.total_datas;
                ReportChars.networks = o.networks;
                ReportChars.highchars_data = o.highchars_data;
                ReportChars.data.xAxis.categories = o.createdTime;
                ReportChars.open_highchart();
                Report.is_slot_change = true;
                Report.set_network(o.network_detail_data);
                Report.table = o.table_data;
                Report.foot = o.total_datas;
                $.unblockUI()
            }
        })
    },

    get_report_stats_country: function(){
        Report.date_or_country = 'country'
        var data = {
            start: Report.start,
            end: Report.end,
            slot: Report.slot,
            date_or_country: 'country'
        }
        $.blockUI({
            css : {
                top: '400px'
            }
        })
        $.postJSON1("/report/stats", data, function (o) {
            if(!o.err){
                Report.network_detail_data = o.network_detail_data;
                Report.table_data = o.table_data;
                Report.total_datas = o.total_datas;
                Report.foot_total_datas = o.total_datas;
                Report.set_network(o.network_detail_data);
                Report.table = o.table_data;
                Report.foot = o.total_datas;
                $.unblockUI()
                $('#container, #btn-box').hide();
            }
        })
    },
    get_report_stats_slot: function(){
        Report.date_or_country = 'slot'
        var data = {
            start: Report.start,
            end: Report.end,
            date_or_country: 'slot'
        }
        $.blockUI({
            css : {
                top: '400px'
            }
        })
        $.postJSON1("/report/stats", data, function (o) {
            if(!o.err){
                Report.network_detail_data = o.network_detail_data;
                Report.table_data = o.table_data;
                Report.total_datas = o.total_datas;
                Report.foot_total_datas = o.total_datas;
                Report.set_network(o.network_detail_data);
                Report.table = o.table_data;
                Report.foot = o.total_datas;
                $.unblockUI()
                $('#container, #btn-box').hide();
            }
        })
    },
    is_slot_change: false,
    slot_change: function(){
        if(Report.is_slot_change){
            if(Report.date_or_country == 'country'){
                Report.get_report_stats_country();
            }else{
                Report.get_report_stats();
            }
        }
    },

    desc: true,
    sort: function(li, key){
        avalon.vmodels.report[li].sort(function(a,b){
            if(!isNaN(b[key])){
                b[key] = parseFloat(b[key])
            }
            if(!isNaN(a[key])){
                a[key] = parseFloat(a[key])
            }

            if (avalon.vmodels.report.desc){
                if(isNaN(b[key] - a[key])){
                    return b[key] > a[key]
                }else{
                    return b[key] - a[key];
                }
            }else{
                if(isNaN(a[key] - b[key])){
                    return a[key] > b[key]
                }else{
                    return a[key] - b[key];
                }
            }
        });
        avalon.vmodels.report.desc = !avalon.vmodels.report.desc
    },
    click_all:function(){
        Report.table = Report.table_data;
        Report.foot = Report.foot_total_datas;
    },
    set_network:function(data){
        data.forEach(function(e){
            for (k in e) {
                k_s = k
                k = "'"+ k + "'"
            if (document.getElementsByName(k_s).length == 0){
                $("#all").after('<li role="presentation" onclick="click_other('+k+')"><a href="#" style="color:#216fc8" name="'+k_s+'">'+k_s+'</a></li>')
            }
            }
        })
    },
})



Highcharts.setOptions({
    colors: ['#FF8484', '#4DCCCC', '#41CC41', '#FFC24A', '#A56DDD', '#4874A9', '#FF9655', '#FFF263', '#6AF9C4']
});
var ReportChars;
ReportChars = avalon.define({
    $id: 'reportcharts',
    highchars_data: {},

    networks: [],

    data: {
        title: {
            text: '',
        },
        credits: {
            enabled: false
        },
        xAxis: {
            categories: ['2/26', '2/27', '2/28', '2/29', '3/1', '3/2','3/3', '3/4', '3/5', '3/6', '3/7', '3/8']
        },
        yAxis: {
            title: {
                text: ''
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#C7D5E5'
            }]
        },
        legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom',
            x:-10
        },
        series: [
            {
                name: 'Tokyo',
                data: [7.0, 6.9, 9.5, 14.5, 18.2, 210.5]
            },
            {
                name: 'New York',
                data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0]
            },
            {
                name: 'Berlin',
                data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0]
            },
            {
                name: 'London',
                data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2]
            }
        ]
    },

    open_highchart: function(value){
        if(!value) value='show_revenue';
        var series = [];
        var networks = ReportChars.networks.$model;
        var h_data = ReportChars.highchars_data.$model;
        if(h_data){
            for (net in networks){
                var network = networks[net];
                var d = {
                    name: network,
                    data: h_data[network][value]
                }
                series.push(d);
            };
        }
        if(series.length){
            ReportChars.data.series = series;
        }else{
            ReportChars.data.series = [
                {
                    name: 'PingStart',
                    data: [0, 0, 0, 0, 0, 0]
                },
            ]
        }
        $('#container').highcharts(ReportChars.data);
        $.unblockUI()
    },

    button_change: function(){
        $("#btn-box li span").click(function(){
            $("#btn-box li span").removeClass("btn_bg_color");
            $(this).addClass("btn_bg_color");
            var _id = $(this).attr("id");
            ReportChars.open_highchart(_id);
        });
    }
})

