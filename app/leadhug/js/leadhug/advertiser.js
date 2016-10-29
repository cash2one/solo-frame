var advertiser = avalon.define(
    {
        $id:'advertiser',
        status: '',
        ads:[
            {}
        ],
        limit:$("#display").val(),
        totalPage:'',
        ads_count:'',
        status_change: function(e){
            advertiser.status = e.target.value;
        },

        filter:function(){
            var url = '/advertisers/manage/j?status='+ advertiser.status +'&limit='+advertiser.limit+'&page='+'1';
            //console.log(url);
            $.getJSON1(url,{},function(o){
                advertiser.ads = o.ads;
                advertiser.ads_count = o.ads_count;
                advertiser.totalPage = Math.ceil(advertiser.ads_count/advertiser.limit);
                $("#pages").extendPagination({
                        totalCount:advertiser.ads_count,
                        limit:advertiser.limit,
                });
                if($("#pages").html()) $(".page_select").removeClass('hidden');
                $("#pages > ul > li").click(function(){
                    var page = $("#pages .active").text();
                    advertiser.filter_page_ads(page);
                });
            })
        },

        filter_page_ads:function(page){
            var url = '/advertisers/manage/j?status='+ advertiser.status +'&limit='+advertiser.limit+'&page='+ page;
            $.getJSON1(url,{},function(o){
                advertiser.ads = o.ads;
            })
        },

        changeLimit:function(){
            advertiser.filter();
        },

        goPage:function(){
            var page = $("#go-page").val();
            $("#go-page").val('');
            $("#page_" + page).click();
        },
    }
)

var advertiser_account = avalon.define(
    {
        $id:'advertiser_account',
        account_managers:[
            {
                _id: '',
                account: ''
            }
        ],

        pms: [
            {
                _id: '',
                account: ''
            }
        ],

        advertiser: {
            _id: '',
            name:'',
            email:'',
            country:'',
            account_manager:'',
            pm:'',
            skype_id:'',
            status: '',
            white_list: ''
        },
        user:'',
        status_change: function(e){
            advertiser_account.advertiser.status = e.target.value;
        },
        account_change: function(e){
            advertiser_account.advertiser.account_manager = e.target.value;
        },

        save: function(val){
            var url;
            if(val == 'new'){
                url = '/advertisers/new/';
            }else{
                url = '/advertisers/update/'+advertiser_account.advertiser._id;
            }

             $.postJSON1(url, advertiser_account.advertiser, function(o) {
                 if (!o.err) {
                     location.href = '/advertiser/detail/'+ o.advertiser_id
                 }else{
                    $(".err").remove();
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("#"+k).after('<div class="err" style="color: red">'+v+"</div>")
                    }
                 }
            });
        }
    }
)
