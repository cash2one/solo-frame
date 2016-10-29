var Offer = avalon.define({
    $id: 'Offer',

    filter: {
        _type: '',
        countries: '',
        price_model: '',
        categories: '',
        access_status: '',
        approvalStatus: '',
        payoutMin: '0.000',
        payoutMax: '10000',
        offerSearch: '',
        limit: '',
        page: ''
    },

    categories: [
        {}
    ],

    countries: [],

    Search: function(val){
        if(val == 'applyoffers'){
            Offer.filter._type = 'applied'
        }else{
            Offer.filter._type = 'need_approived'
        }
        var node = $("#"+val);
        Offer.filter.countries = $(".country_1", node).val();
        Offer.filter.price_model = $(".price_model_1", node).val();
        Offer.filter.categories = $(".categories_1", node).val();
        Offer.filter.access_status = $("#access_status", node).val();
        Offer.filter.approvalStatus = $("#approvalStatus", node).val();
        Offer.filter.limit = Offer.limit;
        Offer.filter.page = 1;

        $.blockUI({
            css : {
                top: '400px'
            }
        })

        $.getJSON1('/offers/search', Offer.filter, function(o){
                Offer.offers = o.offers;
                Offer.offers_count = o.offers_count;
                Offer.totalPage = Math.ceil(Offer.offers_count/Offer.limit);
                $("#pages_1").extendPagination({
                    totalCount: Offer.offers_count,
                    limit: Offer.limit
                });
                if($("#pages_1").html()) $(".page1_select").removeClass('hidden');
                $("#pages_1 > ul > li").click(function(){
                    var page = $("#pages_1 .active").text();
                    Offer.get_page_offers(page, node);
                })
                $.unblockUI();
        });
    },
    get_page_offers: function(page, node){
        Offer.filter.countries = $(".country_1", node).val();
        Offer.filter.price_model = $(".price_model_1", node).val();
        Offer.filter.categories = $(".categories_1", node).val();
        Offer.filter.access_status = $("#access_status", node).val();
        Offer.filter.approvalStatus = $("#approvalStatus", node).val();
        Offer.filter.limit = Offer.limit;
        Offer.filter.page = page;
        $.blockUI({
                css : {
                    top: '400px'
                }
            })
        $.getJSON1('/offers/search', Offer.filter, function(o){
                Offer.offers = o.offers;
                $(".select_all").removeAttr('checked');
                $.unblockUI();
        });
    },
    changeLimit: function(){
        Offer.Search('searchoffers');
    },
    goPage:function(){
        var page = $("#go-page1").val();
        $("#go-page1").val('');
        $("#page_"+page).click();
    },
    offers: [
        {

        }
    ],

    my_offers: [
        {

        }
    ],

    offers_count: '',
    limit: $("#display1").val(),
    totalPage:'',

    ApplyList: function(){
        var apply_select = $(".apply_select");
        var apply_list = [];
        $.each(apply_select, function(i, thiz){
            if($(thiz).attr('checked') == 'checked'){
                apply_list.push($(thiz).attr('offer_id'))
            }
        })
        if(!apply_list.length)return;
        Offer.Apply(apply_list);
    },
    Apply: function(offer){
        var apply_ids = [];
        if(!Array.isArray(offer)){
            apply_ids.push(offer._id);
        }else{
            apply_ids = offer;
        }
        $.postJSON1('/offers/apply', {'_ids': apply_ids}, function(o){
                if(!o.err){
                    location.reload();
                }else{
                    $.Prompt(o.err.apply);
                }
            });
    }
})


var ApplyOffer = avalon.define({
    $id: 'ApplyOffer',

    filter: {
        _type: '',
        countries: '',
        price_model: '',
        categories: '',
        access_status: '',
        approvalStatus: '',
        payoutMin: '0.000',
        payoutMax: '10000',
        offerSearch: '',
        limit: '',
        page: ''
    },

    categories: [
        {}
    ],

    countries: [],

    Search: function(val){
        if(val == 'applyoffers'){
            ApplyOffer.filter._type = 'applied'
        }else{
            ApplyOffer.filter._type = 'need_approived'
        }
        var node = $("#"+val);
        ApplyOffer.filter.countries = $(".country_1", node).val();
        ApplyOffer.filter.price_model = $(".price_model_1", node).val();
        ApplyOffer.filter.categories = $(".categories_1", node).val();
        ApplyOffer.filter.access_status = $("#access_status", node).val();
        ApplyOffer.filter.approvalStatus = $("#approvalStatus", node).val();
        ApplyOffer.filter.limit = ApplyOffer.limit;
        ApplyOffer.filter.page = 1;
        $.blockUI({
            css : {
                top: '400px'
            }
        })
        $.getJSON1('/offers/search', ApplyOffer.filter, function(o){
                ApplyOffer.offers = o.offers;
                ApplyOffer.offers_count = o.offers_count;
                ApplyOffer.totalPage = Math.ceil(ApplyOffer.offers_count/ApplyOffer.limit);
                $("#pages_applied").extendPagination({
                    totalCount: ApplyOffer.offers_count,
                    limit: ApplyOffer.limit,
                });
                 if($("#pages_applied").html()) $(".page2_select").removeClass('hidden');
                $("#pages_applied > ul > li").click(function(){
                    var page = $("#pages_applied .active").text();
                    //ApplyOffer.get_page_offers(page, node);
                    ApplyOffer.get_page_offers(page, node);
                })
                $.unblockUI();
        });
    },
    get_page_offers: function(page, node){
        ApplyOffer.filter.countries = $(".country_1", node).val();
        ApplyOffer.filter.price_model = $(".price_model_1", node).val();
        ApplyOffer.filter.categories = $(".categories_1", node).val();
        ApplyOffer.filter.access_status = $("#access_status", node).val();
        ApplyOffer.filter.approvalStatus = $("#approvalStatus", node).val();
        ApplyOffer.filter.limit = ApplyOffer.limit;                       //BUG GOES HERE!!!!!!!!!!!!!
        ApplyOffer.filter.page = page;
        $.blockUI({
            css : {
                top: '400px'
            }
        })
        $.getJSON1('/offers/search', ApplyOffer.filter, function(o){     //bug goes here!!!!!!!!!!!!!!
                ApplyOffer.offers = o.offers;
                $.unblockUI();
        });
    },
    changeLimit:function(){
        ApplyOffer.Search('applyoffers')
    },
    goPage:function(){
        var page = $("#go-page2").val();
        $("#go-page2").val('');
        var node = $("#applyoffers")
        $("#pages_applied #page_"+page).click();
    },

    offers: [
        {

        }
    ],

    my_offers: [
        {

        }
    ],

    offers_count: '',
    limit: $("#display2").val(),
    totalPage:'',
})


var MyOffer = avalon.define({
    $id: 'my_offer',

    filter: {
        countries: '',
        price_model: '',
        categories: '',
        payoutMin: '0.000',
        payoutMax: '10000',
        is_api: '0'
    },

    categories: [
        {}
    ],
    countries: [],

    Search: function(){
        MyOffer.filter.countries = $("#country_2").val();
        MyOffer.filter.price_model = $("#price_model_2").val();
        MyOffer.filter.categories = $("#categories_2").val();
        MyOffer.filter.is_api = $("#is_api").val();
        MyOffer.filter.limit = MyOffer.limit;
        MyOffer.filter.page = 1;
        $.blockUI({
            css : {
                top: '400px'
            }
        })
        $.getJSON1('/my_offers/search', MyOffer.filter, function(o){
                MyOffer.my_offers = o.offers;
                MyOffer.offers_count = o.offers_count;
                MyOffer.totalPage = Math.ceil(MyOffer.offers_count/MyOffer.limit);
                $("#pages_2").extendPagination({
                        totalCount: MyOffer.offers_count,
                        limit: MyOffer.limit
                    });

                    if($("#pages_2").html()) $(".page3_select").removeClass('hidden');
                    $("#pages_2 > ul > li").click(function(){
                        var page = $("#pages_2 .active").text();
                        MyOffer.get_page_offers(page);
                    })
            $.unblockUI();
        });
    },

    get_page_offers: function(page){
        MyOffer.filter.countries = $("#country_2").val();
        MyOffer.filter.price_model = $("#price_model_2").val();
        MyOffer.filter.categories = $("#categories_2").val();
        MyOffer.filter.is_api = $("#is_api").val();
        MyOffer.filter.limit = MyOffer.limit;
        MyOffer.filter.page = page;
        $.getJSON1('/my_offers/search', MyOffer.filter, function(o){
                MyOffer.my_offers = o.offers;
        });
    },
    changeLimit: function(){
        MyOffer.Search();
    },
    goPage: function(){
        var page = $("#go-page3").val();
        $("#go-page3").val();
        $("#pages_2 #page_"+page).click();
    },
    my_offers: [
        {

        }
    ],

    offers_count: '',
    limit: $("#display3").val(),
    totalPage: '',
})

var OfferDetail = avalon.define({
    $id: 'offer_detail',

    offer: {

    },
    aff_id:'',
    tracking_link: 'http://track.leadhug.com/tl?a=',
    click_id:'',
    sub_id_1:'',
    sub_id_2:'',
    sub_id_3:'',
    sub_id_4:'',
    sub_id_5:'',


    Apply: function(obj){
        $.postJSON1('/offers/apply', {'_id': obj._id}, function(o){
                if(!o.err){
                    location.reload();
                }
            });
    }
})

var offer_tab = avalon.define({
    $id: 'offer_tab',

    search: function(){
        Offer.Search('searchoffers');
    },

    apply_search: function(){
        ApplyOffer.Search('applyoffers');
    },

    my_search: function(){
        MyOffer.Search();
    }
})
