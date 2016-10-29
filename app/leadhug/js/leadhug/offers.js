var offer = avalon.define(
    {
        $id:'offer',
        offers:[
            {}
        ],
        cat:[
            {}
        ],
        ads:[
            {}
        ],
        offer:{
            geo_targeting: [],
            exclude_geo_targeting: [],
        },
        url_banner:'',
        url_cover:'',
        include_or_exclude: '1',

        limit: $("#display").val(),
        totalPage: '',

        filter: {
            offer_ids: [],
            is_api: '0',
            status: '',
            category: '',
            price_model: '',
            advertiser: '',
            geo: '',
            payout_min: '',
            payout_mix: '',
	    page: 1,
	    limit: '',
        },
        offers_count:'',

        report_export: function(){
            var _url = '/report/export?filter=' + JSON.stringify(avalon.vmodels.offer.filter)
            location.href = _url;
        },

        get_report: function(){
            $.blockUI({
                css : {
                    top: '400px'
                }
            });
            offer.filter.offer_ids = [];
            $(".token-input-list .token-input-token > p").each(function(){
                var value = $(this).text();
                if(typeof value === 'string'){
                    offer.filter.offer_ids.push(value.split(' ')[0])
                }
            })
            offer.filter.limit = offer.limit;
            $.postJSON1('/j/offers/manager', offer.filter, function(o){
                offer.offers = o.offers;
                offer.advertisers = o.advertisers;
                offer.categories = o.categories;
                offer.offers_count = o.offers_count
                offer.totalPage = Math.ceil(offer.offers_count/offer.limit)

                $("#pages").extendPagination({
                    totalCount: offer.offers_count,
                    limit: offer.limit
                });
                if($("#pages").html()) $(".page_select").removeClass('hidden');
                $("#pages > ul > li").click(function(){
                    var page = $("#pages .active").text();
                    offer.get_page_report(page);
                });
                $.unblockUI()
            });
        },

        get_page_report: function(page){
            offer.filter.page = page
            $.blockUI({
                    css : {
                        top: '400px'
                    }
                })
            $.postJSON1('/j/offers/manager', offer.filter, function(o){
                offer.offers = o.offers;
                offer.advertisers = o.advertisers;
                offer.categories = o.categories;
                offer.filter.page = '1';
                $.unblockUI()
            });
        },


        changeLimit:function(){
            offer.get_report();
        },  

        goPage:function(){
            var page = $("#go-page").val();
            $("#go-page").val('');
            $("#page_"+page).click();
        }, 

        mouseover: function(data){
             $(".geo", $(this)).hide();
             $(".geo-info", $(this)).show('fast');
        },

        mouseout: function(){
            $(".geo-info", $(this)).hide();
            $(".geo", $(this)).show();
        },

        pause_offer: {
            offer_id: '',
            offer_name: '',
            pause_date: '',
        },
        pause_offer_select: function(offer_select){
            offer.pause_offer.offer_id = offer_select._id;
            offer.pause_offer.offer_name = offer_select.title;
            $(".dp_start").val('');
        },

        pause_task_close: function(){
            offer.pause_offer.offer_id = '';
            offer.pause_offer.offer_name = '';
            offer.pause_offer.pause_date = '';
        },

        pause_task: function(){
            $.postJSON1('/offer/pause/add', offer.pause_offer, function(o){
                if(!o.err){
                    $("#offer_"+offer.pause_offer.offer_id).addClass('hidden');
                    $(".offer_pause_close").click();
                }else{
                    $(".err").remove();
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("."+k).after('<div class="err" style="color: red">'+v+"</div>")
                    }
                }
            });
        }
    }
)
var advertiser = avalon.define(
        {
            $id: 'advertiser',
            advertisers:[
                     {}
           ],
        }
)

var category = avalon.define(
        {
            $id: 'category',
            categories:[
                     {}
            ],
        }
)
