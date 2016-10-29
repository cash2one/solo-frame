var Payment = avalon.define({
    $id: 'payment',
    invoices: [
        {
            createdTime: '',
            time_range: {},
            _invoice_number: '',
            _invoice: {
                real_pay: '100'
            }
        }
    ],

    limit: $("#display").val(),
    totalPage: '',

    get_payments: function(){
        var o = {'limit': Payment.limit, 'page': 1};
        $.postJSON1('/j/payments', o , function(o){
            Payment.invoices = o.invoices;
            Payment.invoices_count = o.invoices_count;
            Payment.totalPage = Math.ceil(Payment.invoices_count/Payment.limit);;
            $("#pages").extendPagination({
                totalCount: Payment.invoices_count,
                limit: Payment.limit
            });
             if($("#pages").html()) $(".page_select").removeClass('hidden');
            $("#pages > ul > li").click(function(){
                var page = $("#pages .active").text();
                Payment.get_page_payments(page);
            })
        });
    },

    get_page_payments: function(page){
        $.postJSON1('/j/payments', {'limit': Payment.limit, 'page': page}, function(o){
            Payment.invoices = o.invoices;
        });
    },

    changeLimit:function(){
        Payment.get_payments();
    },
    goPage:function(){
        var page = $("#go-page").val();
        $("#go-page").val('');
        $("#page_"+page).click();
    },
})

