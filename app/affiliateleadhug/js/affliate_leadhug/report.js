var Report = avalon.define({
    $id: 'report',

    countries: [],
    offers: [
        {}
    ],


    payout_is_zero: true,

    doc_count: 0,
    limit: $("#display").val(),
    totalPage:'',

    total: '',
    fields: {
        year: false,
        month: false,
        week: false,
        day: true,
        hour: false,
        affiliate_sub_id_1: false,
        affiliate_sub_id_2: false,
        affiliate_sub_id_3: false,
        affiliate_sub_id_4: false,
        affiliate_sub_id_5: false,
        offer_name: false,
        offer_id: false,
        country: false,
        impressions: true,
        clicks: true,
        unique_clicks: true,
        gross_clicks: false,
        cost: true,
        conversions: true,
        CTR: false,
        CPM: false,
        CPC: false,
        CPA: false,
        CR: true,
        RPM: false,
        RPC: false,
        RPA: false,
        EPC: true,
    },

    filter: {
        affiliates_name: [],
        offers_id: [],
        countries: [],
        payout_types: [],

        time_range: {
            start: '',
            end: ''
        }
    },

    payout_range: {
        min: '0.000',
        mix: '10000'
    },

    docs: [
        {
            _id: '',
            year: '',
            month: '',
            week: '',
            day: '',
            hour: '',
            offer_name: '',
            offer_id: '',
            affiliate_sub_id_1: '',
            affiliate_sub_id_2: '',
            affiliate_sub_id_3: '',
            affiliate_sub_id_4: '',
            affiliate_sub_id_5: '',
            advertiser_name: '',
            country: '',
            clicks: '',
            unique_clicks: '',
            gross_clicks: '',
            revenue: '',
            cost: '',
            conversions: '',
            CTR: '',
            CPM: '',
            CPC: '',
            CPA: '',
            CR: '',
            RPM: '',
            RPC: '',
            RPA: '',
            EPC: '',
        }
    ],

    report_url: '',

    get_report_url: function(){
        var _url  = '/j/export_report?fields=';
        _url += JSON.stringify(Report.fields);
        _url += '&filter='
        _url += JSON.stringify(Report.filter);
        _url += '&payout_is_zero=';
        _url += Report.payout_is_zero;
        _url += '&payout_range=';
        _url += JSON.stringify(Report.payout_range);
        Report.report_url = _url;
    },

    get_report: function(){
            var args = {
                'fields': Report.fields,
                'filter': Report.filter,
                'start': Report.filter.time_range.start,
                'end': Report.filter.time_range.end,
                'payout_is_zero': Report.payout_is_zero,
                'payout_range': Report.payout_range,
                'limit': Report.limit,
                'page': 1
            }

            $.blockUI({
                css : {
                    top: '400px'
                }
            })

            $.postJSON1('/j/report', args, function(o){
                if(!o.docs){
                    $.unblockUI();
                    alert("The result exceeds maximum size!");
                    return;
                }
                Report.docs = o.docs;
                Report.doc_count = o.doc_count;
                Report.total = o.total;
                Report.totalPage = Math.ceil(Report.doc_count/Report.limit);
                $("#pages").extendPagination({
                    totalCount: Report.doc_count,
                    limit: Report.limit
                });
                if($("#pages").html()) $(".page_select").removeClass('hidden');
                $("#pages > ul > li").click(function(){
                    var page = $("#pages .active").text();
                    Report.get_page_report(page);
                })
                $.unblockUI()
            });

            Report.get_report_url();
        },

    get_page_report: function(page){
        var args = {
            'fields': Report.fields,
            'filter': Report.filter,
            'start': Report.filter.time_range.start,
            'end': Report.filter.time_range.end,
            'payout_is_zero': Report.payout_is_zero,
            'payout_range': Report.payout_range,
            'limit': Report.limit,
            'page': page
        }

        $.blockUI({
                css : {
                    top: '400px'
                }
            })
        $.postJSON1('/j/report', args, function(o){
            Report.docs = o.docs;
            Report.total = o.total;
            $.unblockUI()
        });
    },

    changeLimit:function(){
        Report.get_report();
    },
    goPage:function(){
        var page = $("#go-page").val();
        $("#go-page").val('');
        $("#page_"+page).click();
    },

    report_export: function(){
        var args = {
            'fields': Report.fields,
            'filter': Report.filter,
            'start': Report.filter.time_range.start,
            'end': Report.filter.time_range.end,
            'payout_is_zero': Report.payout_is_zero,
            'payout_min': Report.payout_range.min,
            'payout_mix': Report.payout_range.mix,
            'limit': Report.limit,
            'page': 1
        }
        $.getJSON1('/j/export_report', args, function(o){
            return o;
        });
    },

})

$(function() {
            $("#report").addClass('active');
            $(".reports-select").val('').multipleSelect();
            $("#country_1").val('');
            function cb(start, end) {
                $('#reportrange span').html(start.format('YYYY-MM-DD') + ' -- ' + end.format('YYYY-MM-DD'));
            }
            cb(moment().subtract(3, 'days'), moment());

            $('#reportrange').daterangepicker({
                ranges: {
                   'Today': [moment(), moment()],
                   'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                   'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                   'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                   'This Month': [moment().startOf('month'), moment().endOf('month')],
                   'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                }
            }, cb);

            function cb2(start, end) {
                $('#reportrange2 span').html(start.format('YYYY-MM-DD') + ' -- ' + end.format('YYYY-MM-DD'));
            }
            cb2(moment().subtract(3, 'days'), moment());

            $('#reportrange2').daterangepicker({
                ranges: {
                   'Today': [moment(), moment()],
                   'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                   'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                   'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                   'This Month': [moment().startOf('month'), moment().endOf('month')],
                   'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                }
            }, cb2);
});
