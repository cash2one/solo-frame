var Dashboard=avalon.define({
    $id: 'dashboard',
    publisher:'',
    slot:'',
    time:true,
    country:false,
    new_data:'',
    active_data:'',
    total_data:'',
    time_count: 0,
    country_count:0,
    limit:10,
    filter:{
        time:{},
        publisher_id:'',
        slot_id:'',
    },
    data_group_by_time:'',
    data_group_by_time_slice:'',
    data_group_by_country:'',
    data_group_by_country_slice:'',
    time_url:'',
    get_time_url: function(){
        var _url  = '/j/export/time?filter=';
        _url += JSON.stringify(Dashboard.filter);
        Dashboard.time_url = _url;
    },
    country_url:'',
    get_country_url: function(){
        var _url  = '/j/export/country?filter=';
        _url += JSON.stringify(Dashboard.filter);
        Dashboard.country_url = _url;
    },
    get_slot: function(publisher_id){
        $.getJSON1(
            "/j/get_slot",
            {'publisher_id':publisher_id},
            function(o){
                Dashboard.filter.publisher_id = publisher_id;
                Dashboard.slot = o.slot;
                Dashboard.get_data();
            }
        )
    },
    get_data: function(slot_id){
        Dashboard.filter.slot_id = slot_id;
        $.postJSON1(
            "/j/dashboard",
            avalon.vmodels.dashboard.filter.$model,
            function(o){
                Dashboard.time_count = o.sort_by_time.count
                Dashboard.country_count = o.sort_by_country.count
                Dashboard.data_group_by_country = o.sort_by_country.sort_by_country;
                Dashboard.data_group_by_time = o.sort_by_time.sort_by_time;
                Dashboard.data_group_by_time_slice = Dashboard.data_group_by_time.$model.slice(0,Dashboard.limit);
                Dashboard.data_group_by_country_slice = Dashboard.data_group_by_country.$model.slice(0,Dashboard.limit);
                $("#pages_time").extendPagination({
                    totalCount: Dashboard.time_count,
                    limit: Dashboard.limit
                });
                $("#pages_time > ul > li").click(function(){
                    var page = $("#pages_time .active").text();
                    Dashboard.data_group_by_time_slice = Dashboard.data_group_by_time.$model.slice(Dashboard.limit * (page - 1),Dashboard.limit * page);

                })

                $("#pages_country").extendPagination({
                    totalCount: Dashboard.country_count,
                    limit: Dashboard.limit
                });
                $("#pages_country > ul > li").click(function(){
                    var page = $("#pages_country .active").text();
                    Dashboard.data_group_by_country_slice = Dashboard.data_group_by_country.$model.slice(Dashboard.limit * (page - 1),Dashboard.limit * page);
                })
            }
        );
        $.postJSON1(
            "/j/charts",
            Dashboard.filter.$model,
            function(o){
                Dashboard.new_data = o.new_data;
                var charts = $('#container').highcharts();
                charts.series[0].update({data:Dashboard.new_data.y});
                charts.xAxis[0].update({categories:Dashboard.new_data.x})
            }
        );
        Dashboard.get_country_url();
        Dashboard.get_time_url();
    },
    status_time: function(){
        $('#time').click(function(){
            Dashboard.time = true;
            Dashboard.country = false;
        });
    },
    status_country: function(){
        $('#country').click(function(){
            Dashboard.country = true;
            Dashboard.time = false;
        })
    },
    get_new:function(){
        $.postJSON1(
            "/j/charts",
            Dashboard.filter.$model,
            function(o){
                Dashboard.new_data = o.new_data;
                var charts = $('#container').highcharts();
                charts.series[0].update({data:Dashboard.new_data.y});
                charts.xAxis[0].update({categories:Dashboard.new_data.x})
            }
        )
    },
    get_active: function(){
        $.postJSON1(
            "/j/charts",
            Dashboard.filter.$model,
            function(o){
                Dashboard.active_data = o.active_data;
                var charts = $('#container').highcharts();
                charts.series[0].update({data:Dashboard.active_data.y});
                charts.xAxis[0].update({categories:Dashboard.active_data.x})
            }
        )
    },
    get_total:function(){
        $.postJSON1(
            "/j/charts",
            Dashboard.filter.$model,
            function(o){
                Dashboard.total_data = o.total_data;
                var charts = $('#container').highcharts();
                charts.series[0].update({data:Dashboard.total_data.y});
                charts.xAxis[0].update({categories:Dashboard.total_data.x})
            }
        )
    }
})

$(function() {
    var today = new Date().Format("yyyy-MM-dd");
    var before = GetLastWeekDate()
    $('input[name="daterange"]').daterangepicker({
        'startDate':before,
        'endDate':today,
        'locale': {
            format: 'YYYY-MM-DD'
    }
    });
    $('input[name="daterange"]').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
        avalon.vmodels.dashboard.filter.time = {'start': picker.startDate.format('YYYY-MM-DD'), 'end': picker.endDate.format('YYYY-MM-DD')};
        $.postJSON1(
        "/j/dashboard",
        avalon.vmodels.dashboard.filter.$model,
        function(o){
            Dashboard.time_count = o.sort_by_time.count
            Dashboard.country_count = o.sort_by_country.count
            Dashboard.data_group_by_country = o.sort_by_country.sort_by_country;
            Dashboard.data_group_by_time = o.sort_by_time.sort_by_time;
            Dashboard.data_group_by_time_slice = Dashboard.data_group_by_time.$model.slice(0,Dashboard.limit);
            Dashboard.data_group_by_country_slice = Dashboard.data_group_by_country.$model.slice(0,Dashboard.limit);
            $("#pages_time").extendPagination({
                totalCount: Dashboard.time_count,
                limit: Dashboard.limit
            });
            $("#pages_time > ul > li").click(function(){
                var page = $("#pages_time .active").text();
                Dashboard.data_group_by_time_slice = Dashboard.data_group_by_time.$model.slice(Dashboard.limit * (page - 1),Dashboard.limit * page);
            })
            $("#pages_country").extendPagination({
                totalCount: Dashboard.country_count,
                limit: Dashboard.limit
            });
            $("#pages_country > ul > li").click(function(){
                var page = $("#pages_country .active").text();
                Dashboard.data_group_by_country_slice = Dashboard.data_group_by_country.$model.slice(Dashboard.limit * (page - 1),Dashboard.limit * page);
            })
        }
        );
        $.postJSON1(
            "/j/charts",
            Dashboard.filter.$model,
            function(o){
                Dashboard.new_data = o.new_data;
                var charts = $('#container').highcharts();
                charts.series[0].update({data:Dashboard.new_data.y});
                charts.xAxis[0].update({categories:Dashboard.new_data.x})
            }
        );
        Dashboard.get_country_url();
        Dashboard.get_time_url();
         });
    $('input[name="daterange"]').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
        avalon.vmodels.dashboard.filter.time = ''
        $.postJSON1(
            "/j/dashboard",
            avalon.vmodels.dashboard.filter.$model,
            function(o){
                Dashboard.time_count = o.sort_by_time.count
                Dashboard.country_count = o.sort_by_country.count
                Dashboard.data_group_by_country = o.sort_by_country.sort_by_country;
                Dashboard.data_group_by_time = o.sort_by_time.sort_by_time;
                Dashboard.data_group_by_time_slice = Dashboard.data_group_by_time.$model.slice(0,Dashboard.limit);
                Dashboard.data_group_by_country_slice = Dashboard.data_group_by_country.$model.slice(0,Dashboard.limit);
                $("#pages_time").extendPagination({
                totalCount: Dashboard.time_count,
                limit: Dashboard.limit
                });
                $("#pages_time > ul > li").click(function(){
                    var page = $("#pages_time .active").text();
                    Dashboard.data_group_by_time_slice = Dashboard.data_group_by_time.$model.slice(Dashboard.limit * (page - 1),Dashboard.limit * page);
                    console.log(Dashboard.data_group_by_time_slice)
                })

                $("#pages_country").extendPagination({
                    totalCount: Dashboard.country_count,
                    limit: Dashboard.limit
                });
                $("#pages_country > ul > li").click(function(){
                    var page = $("#pages_country .active").text();
                    Dashboard.data_group_by_country_slice = Dashboard.data_group_by_country.$model.slice(Dashboard.limit * (page - 1),Dashboard.limit * page);
                })
            }
         );
         $.postJSON1(
            "/j/charts",
            Dashboard.filter.$model,
            function(o){
                Dashboard.new_data = o.new_data;
                var charts = $('#container').highcharts();
                charts.series[0].update({data:Dashboard.new_data.y});
                charts.xAxis[0].update({categories:Dashboard.new_data.x})
            }
        );
        Dashboard.get_country_url();
        Dashboard.get_time_url();
    });
})