var date = Pingstart;
var report = avalon.define(
    {
        $id: 'report',
        query_fields: {
            hour: false,
            day: true,
            week: false,
            month: false,
            year: false,
            affiliate_name: false,
            affiliate_id: false,
            affiliate_sub_id_1: false,
            affiliate_sub_id_2: false,
            affiliate_sub_id_3: false,
            affiliate_sub_id_4: false,
            affiliate_sub_id_5: false,
            offer_name: false,
            api_offer_name: false,
            offer_id: false,
            advertiser_name: false,
            category_name: false,
            country: false,
            impressions: false,
            clicks: false,
            unique_clicks: false,
            gross_clicks: true,
            revenue: false,
            sales: false,
            cost: true,
            profit: true,
            conversions: true,
            CTR: false,
            CPM: false,
            CPC: true,
            CPA: false,
            CR: false,
            RPM: false,
            RPC: true,
            RPA: false,
        },

        filter: {
            affiliate: false,
            affiliate_show: 'all',
            advertiser: false,
            category: false,
            offers: false,
            ams: false,
            bds: false,
        },

        selected_filter: {
            affiliates_name: [],
            advertisers_name: [],
            categories_name: [],
            offers_id: [],
            ams_id: [],
            bds_id:[],
        },

        time_range: {
            start: date.getBeforeDate(3),
            end: date.getBeforeDate(0)
        },

        conversions_is_zero: true,

        docs: [
            {
                _id: '',
                year: '',
                month: '',
                week: '',
                day: '',
                hour: '',
                affiliate_name: '',
                affiliate_id: '',
                affiliate_sub_id: '',
                offer_name: '',
                offer_id: '',
                affiliate_sub_id_1: '',
                affiliate_sub_id_2: '',
                affiliate_sub_id_3: '',    
                affiliate_sub_id_4: '',
                affiliate_sub_id_5: '',
                advertiser_name: '',
                category_name: '',
                country: '',
                impressions: '',
                clicks: '',
                unique_clicks: '',
                gross_clicks: '',
                revenue: '',
                sales: '',
                cost: '',
                profit: '',
                conversions: '',
                CTR: '',
                CPM: '',
                CPC: '', 
                CPA: '',
                CR: '',
                RPM: '',
                RPC: '',
                RPA: '',
                date: ''
            }
        ],

        doc_count: 0,
        limit: $("#display").val(),
        totalPage:'',

        total: {

        },

        categories: [
            {
                _id: '',
                name: '',
            }
        ],

        affiliates: [
            {
                _id: '',
                name: ''
            }
        ],

        advertisers: [
            {
                _id: '',
                name: '',
            }
        ],

        offers: [
            {
                _id: '',
                title: '',
            }
        ],

        ams: [
            {
                _id: '',
                account: ''
            }
        ],

        bds: [
            {
                _id: '',
                account: ''
            }
        ],


        get_filters: function(){
            $.getJSON1('/j/report/filters', {}, function(o){
                report.offers = o.offers;
                report.affiliates = o.affiliates;
                report.advertisers = o.advertisers;
                report.categories = o.categories;
                report.ams = o.ams;
                report.bds = o.bds;
            })
        },


        get_report: function(){
            var args = {
                'query_fields': report.query_fields,
                'selected_filter': report.selected_filter,
                'start': report.time_range.start,
                'end': report.time_range.end,
                'conversions_is_zero': report.conversions_is_zero,
                'limit': report.limit,
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
                report.docs = o.docs;
                report.doc_count = o.doc_count;
                report.total = o.total;
                report.totalPage = Math.ceil(report.doc_count/report.limit);
                $("#pages").extendPagination({
                    totalCount: report.doc_count,
                    limit: report.limit
                });
                if($("#pages").html()) $(".page_select").removeClass('hidden');
                $("#pages > ul > li").click(function(){
                    var page = $(this).find('a').text();
                    if(isNaN(page)) return;
                    report.get_page_report(page);
                })
                $.unblockUI();
            });

            report.get_report_url();
            $('.cancel').click();
        },

        get_page_report: function(page){
            var args = {
                'query_fields': report.query_fields,
                'selected_filter': report.selected_filter,
                'start': report.time_range.start,
                'end': report.time_range.end,
                'conversions_is_zero': report.conversions_is_zero,
                'limit': report.limit,
                'page': page
            }
            $.blockUI({
                css : {
                    top: '400px'
                }
            })
            $.postJSON1('/j/report', args, function(o){
                report.docs = o.docs;
                report.doc_count = o.doc_count;
                report.total = o.total;
                $.unblockUI()
            });
        },

        select_affiliate_multiple: function(){
			$(".select_affiliate").selectator({
				showAllOptionsOnFocus: true,
				keepOpen: true,
                useSearch: true
			});
        },

        select_advertiser_multiple: function(){
			$("#select_advertiser").selectator({
				showAllOptionsOnFocus: true,
				keepOpen: true,
                useSearch: true
			});
        },

        select_category_multiple: function(){
			$("#select_category").selectator({
				showAllOptionsOnFocus: true,
				keepOpen: true,
                useSearch: true
			});
        },

        select_offer_multiple: function(){
            $("#select_offers").selectator({
				showAllOptionsOnFocus: true,
				keepOpen: true,
                useSearch: true
			});
        },

        select_am_multiple: function(){
            $("#select_ams").selectator({
				showAllOptionsOnFocus: true,
				keepOpen: true,
                useSearch: true
			});
        },

        select_bd_multiple: function(){
            $("#select_bds").selectator({
				showAllOptionsOnFocus: true,
				keepOpen: true,
                useSearch: true
			});
        },

        report_url: '',

        get_report_url: function(){
            var _url  = '/j/export_report?fields=';
            _url += JSON.stringify(report.query_fields);
            _url += '&filter='
            _url += JSON.stringify(report.selected_filter);
            _url += '&payout_is_zero=';
            _url += report.conversions_is_zero;
            _url += '&time_range=';
            _url += JSON.stringify(report.time_range);
            report.report_url = _url;
        },


        changeLimit:function(){
            var limit = report.selected;     //limitation to show
            report.get_report();     //re-pager according to the new limitation
        },  
        goPage: function(){
            var page_num = $("#go-page").val();
            $("#go-page").val('');
            $("#page_"+page_num).click();
        },
    }
);
