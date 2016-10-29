var date = Pingstart;
var invoice_list = avalon.define(
    {
        $id: 'invoice_list',

        affiliates: [
            {

            }
        ],
        affiliate_id: '0',

        status: '',

        invoices: [
            {
                _id: '',
                affilicate_id: '',
                _invoice: [
                    {}
                ],
                currency: '',
                time_range: {
                    start: '',
                    end: ''
                },
                createdTime: ''
            }
        ],
        limit: $("#display").val(),
        totalPage:'',
        invoice_count:'',


        time_range: {
            start: date.getBeforeDate(6),
            end: date.getBeforeDate(0)
        },
/*        filter: function(){
            var _url = '/j/invoices?start='+invoice_list.time_range.start+'&end='+invoice_list.time_range.end+'&affiliate_id='+invoice_list.affiliate_id+'&status='+invoice_list.status
            $.getJSON1(_url, {}, function(o){
                invoice_list.invoices = o.invoices;
            })
        },
*/
        filter: function(){
            var _url = '/j/invoices?start='+invoice_list.time_range.start+'&limit='+invoice_list.limit+'&page='+'1'+'&end='+invoice_list.time_range.end+'&affiliate_id='+invoice_list.affiliate_id+'&status='+invoice_list.status
            $.getJSON1(_url, {}, function(o){
                invoice_list.invoices = o.invoices;
                invoice_list.invoice_count = o.invoice_count;
                var limit = invoice_list.limit;
                $("#pages").extendPagination({
                    totalCount:invoice_list.invoice_count,
                    limit:invoice_list.limit
                });
                if($("#pages").html()) $(".page_select").removeClass('hidden');
                $("#pages > ul >li").click(function(){
                    var page = $("#pages .active").text();
                    invoice_list.filter_page_invoice(page);
                });         
            })
        },


        changeLimit:function(){

        },

        goPage:function(){
            var page = $("#go-page").val();
            $("#go-page").val('');
            $("#page_"+page).click();
        }, 

        up_status: function(val){
            var o = {'_id': val};
            $.postJSON1("/j/invoice/update", o, function(o) {
                if (!o.err) {
                    location.reload()
                }
            });
        },

        filter_page_invoice: function(page){
            var _url = '/j/invoices?start='+invoice_list.time_range.start+'&limit='+invoice_list.limit+'&page='+page+'&end='+invoice_list.time_range.end+'&affiliate_id='+invoice_list.affiliate_id+'&status='+invoice_list.status
            $.getJSON1(_url, {}, function(o){
                invoice_list.invoices = o.invoices;
            });
        },
    }
);














var invoice_new = avalon.define(
    {
        $id: 'invoice_new',
        offer_info: [
            {
                offer_id: '',
                paryout: '',
                actions: '',
                amount: '',
                real_pay: '',
                remark: ''

            }
        ],
        affiliates: [
            {

            }
        ],
        affiliates_id: '',  //a bug goes here,i changed it,but not solved!

        currencys: [],
        currency: 'U.S.$',

        time_range: {
            start: date.getBeforeDate(7),
            end: date.getBeforeDate(1)
        },

        filter: function(){
            var _url = '/j/invoice/new?start='+invoice_new.time_range.start+'&end='+invoice_new.time_range.end+'&affiliate_id='+'33'+'&currency='+invoice_new.currency
            $.getJSON1(_url, {}, function(o){
                invoice_new.offer_info = o.offer_info;
                invoice_new.currencys = o.currencys;
            })
        },

        save: function(){
            var o = {
                'affiliate_id': invoice_new.affiliates_id,
                'currency': invoice_new.currency,
                'time_range': invoice_new.time_range,
                '_invoices': invoice_new.offer_info.$model,
            }
            $.postJSON1("/j/invoice/new", o, function(o) {
                if (!o.err) {
                    location.href = '/invoices'
                }
            });
        }
    }
);

avalon.ready(
            function () {

            }
    )
