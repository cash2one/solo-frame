var offer_affiliate = avalon.define(
    {
        $id: 'offer_affiliate',
        offer: {
            black_ip: []
        },

        offers: [
            {}
        ],

        affiliate: {

        },

        affiliates: [
            {}
        ],

        off_affs: [
            {

            }
        ],

        off_aff: {
            affiliate_ids: [],
            offer_ids: [],
            status: '1',
        },

        add_ip: '',

        delete_ip: function(val){
            offer_affiliate.offer.black_ip.remove(val);
            $.postJSON1("/j/offer/update", {'obj': offer_affiliate.offer}, function(o) {
                if (!o.err) {
                    // pass
                }
            });
        },

        add_black_ip: function(e){
            for(var i in offer_affiliate.offer.black_ip){
                if(offer_affiliate.offer.black_ip[i] == offer_affiliate.add_ip.replace(/^\s+|\s+$/g,"")){
                    alert('The Ip has exist!');
                    return;
                }
            }
            offer_affiliate.offer.black_ip.push(offer_affiliate.add_ip.replace(/^\s+|\s+$/g,""));
            $.postJSON1("/j/offer/update", {'obj': offer_affiliate.offer}, function(o) {
                if (!o.err) {
                    location.reload();
                }
            });
        },

        delete_off_aff: function(obj){
            $.postJSON1("/j/offer_affiliate/delete", {'off_aff_id': obj._id}, function(o) {
                location.reload();
            });
        },

        edit_off_aff: function(obj){
            if(obj.affiliate_name){
                var aff_select = {'_id': obj.affiliate_id, 'account': obj.affiliate_name};
                offer_affiliate.affiliates.push(aff_select);
            }else{
                var off_select = {'_id': obj.offer_id, 'title': obj.offer_title};
                offer_affiliate.offers.push(off_select);
            }
            offer_affiliate.off_aff = obj;
        },

        off_aff_update: function(){
            var content = {
                '_id': offer_affiliate.off_aff._id,
                'affiliate_id': offer_affiliate.off_aff.affiliate_id,
                'offer_id': offer_affiliate.off_aff.offer_id,
                'payout': offer_affiliate.off_aff.payout,
                'day_cap': offer_affiliate.off_aff.day_cap,
                'month_cap': offer_affiliate.off_aff.month_cap,
                'total_cap': offer_affiliate.off_aff.total_cap,
                'status': offer_affiliate.off_aff.status
            };
            $.postJSON1("/j/offer_affiliate/update", content, function(o) {
                if (!o.err) {
                    location.reload();
                }
            });
        },

        get_affiliates: function(){
            $.getJSON1("/j/affiliate", {'offer_id': offer_affiliate.offer._id}, function(o) {
                if (!o.err) {
                    offer_affiliate.affiliates = o.affiliates;
                }
            });
        },

        get_offers: function(){
            $.getJSON1("/j/offers", {'affiliate_id': offer_affiliate.affiliate._id}, function(o) {
                if (!o.err) {
                    offer_affiliate.offers = o.offers;
                }
            });
        },

        off_aff_save: function(){
            if(offer_affiliate.off_aff.affiliate_ids.length){
                offer_affiliate.off_aff.offer_id = offer_affiliate.offer._id;
            }else if(offer_affiliate.off_aff.offer_ids.length){
                offer_affiliate.off_aff.affiliate_id = offer_affiliate.affiliate._id;
            }else{
                console.log('offers or affiliates not be empty!');
                $(".err").remove();
                $("#offer_select").after('<div class="err" style="color: red">offers or affiliates not be empty!</div>')
                return;
            }

            $.postJSON1("/j/offer_affiliate/new", offer_affiliate.off_aff, function(o) {
                if (!o.err) {
                    offer_affiliate.off_affs = o.off_affs;
                    location.reload();
                }
            });
        },

        select_plugin_multiple: function(){
			$("#select").selectator({
				showAllOptionsOnFocus: true,
				keepOpen: true
			});
        },

        select_plugin: function(){
			$("#select2").selectator({
				showAllOptionsOnFocus: false,
				keepOpen: false,
                useSearch: false
			});
        },

        mouseover: function(data){
             $(".geo", $(this)).hide();
             $(".geo-info", $(this)).show('fast');
        },

        mouseout: function(){
            $(".geo-info", $(this)).hide();
            $(".geo", $(this)).show();
        },

        post_back: {
            click_url: '',
            redirect_url_list: [
                {
                    'operate': '',
                    'url': ''
                }
            ]
        },
        test_click: function(){
            if(offer_affiliate.post_back.click_url == '')return;
            $.postJSON1("/j/offer_affiliate/post_back/click", {'click_url': offer_affiliate.post_back.click_url}, function(o) {
                if (o.redirect_url_list) {
                    offer_affiliate.post_back.redirect_url_list = o.redirect_url_list;
                }else{
                    offer_affiliate.post_back.redirect_url_list = []
                }
            });
        },
    }
);

