var affiliate = avalon.define(
    {
        $id:'affiliates',
        affs:[
            {}
        ],

        limit:$("#display").val(),
        totalPage: '',
        affs_count:'',


        payment: {
            'payment_method': 'paypal',
            'beneficiary': 'SBS',
            'account_number': '1234567689',
            'bank': 'ICBC',
            'route': 'tcp/ip'
        },

        status: '',


        status_change: function(e){
            affiliate.status = e.target.value;
        },

        filter: function(){
            var url = '/affiliates/manage?status='+affiliate.status+'&limit='+affiliate.limit+'&page='+'1';

            $.postJSON1(url, {}, function(o) {
                 if (!o.err) {
                    affiliate.affs= o.affs
                    affiliate.affs_count = o.affs_count
                    affiliate.totalPage = Math.ceil(affiliate.affs_count/affiliate.limit)
                    $("#pages").extendPagination({
                        totalCount:affiliate.affs_count,
                        limit:affiliate.limit,
                    });
                    if($("#pages").html()) $(".page_select").removeClass('hidden');
                    $("#pages > ul > li").click(function(){
                        var page = $("#pages .active").text();
                        affiliate.filter_page_affs(page);
                    })
                }
            });
        },

        filter_page_affs:function(page){
            var url = '/affiliates/manage?status='+affiliate.status+'&limit='+affiliate.limit+'&page='+page;
            $.postJSON1(url,{},function(o){
                affiliate.affs = o.affs;
            })
        },

        get_payment: function(obj){
            affiliate.payment = obj.payment;
        },


        changeLimit:function(){
            affiliate.filter();
        },  

        goPage:function(){
            var page = $("#go-page").val();
            $("#go-page").val('');
            $("#page_"+page).click();
        },    

    }
)


var affiliate_new = avalon.define(
    {
        $id:'affiliate_new',
        account_managers:[
            {}
        ],

        invoice_frequency: {

        },

        affiliate: {
            account: '',
            email: [],
            country: '',
            account_manager: '',
            skype_id: '',
            company: '',
            status: '1',
            payment: {
                invoice_frequency: '',
                threshold: '',
                payment_method: '',
                beneficiary: '',
                account_number: '',
                bank: '',
                route: '',
                paypal: ''
            }
        },

       save: function(){
            var url = '/affiliate/create';
            if(affiliate_new.affiliate.account_manager == ''){
                affiliate_new.affiliate.account_manager = $("[name=account_manager]").val();
            };
             $.postJSON1(url, affiliate_new.affiliate, function(o) {
                 if (!o.err) {
                    location.href = '/affiliates/manage'
                }else{
                     $(".err").remove();
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("."+k).after('<div class="err" style="color: red">'+v+"</div>")
                    }
                 }
            });
        },
    }
)

var affiliate_modify = avalon.define(
    {
        $id:'affiliate_modify',
        account_managers:[
            {}
        ],

        user: {

        },

        affiliate: {
            account: '',
            email: '',
            country: '',
            account_manager: '',
            skype_id: '',
            company: '',
            status: '',
            payment: {
                invoice_frequency: '',
                threshold: '',
                payment_method: '',
                beneficiary: '',
                account_number: '',
                bank: '',
                route: ''
            }
        },

       save: function(){
            var url = "/affiliates/modify/"+affiliate_modify.affiliate._id;
             $.postJSON1(url, affiliate_modify.affiliate, function(o) {
                 if (!o.err) {
                    location.href = '/affiliates/manage'
                }else{
                     $(".err").remove();
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("."+k).after('<div class="err" style="color: red">'+v+"</div>")
                    }
                 }
            });
        },
    }
)