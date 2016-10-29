var email_list = avalon.define(
    {
        $id: 'email_list',
        emails: [
            {
                _id: '1',
                subject: 'demo',
                sendTime:'2012-02-02'
            }
        ],

        local_storage:[{}],
        emails_count: '',
        limit:$("#display").val(),  
        totalPage:'', 

    get_emails:function(){
        $.blockUI({
            css:{top:"40px"},
        });
        var paras = {};
        paras.page = '1';
        paras.limit = email_list.limit; 
        $.postJSON1('/emails/j',paras,function(o){
            email_list.emails = o.emails;
            email_list.emails_count = o.emails_count;
            email_list.totalPage = Math.ceil(email_list.emails_count/email_list.limit);
            $("#pages").extendPagination({
                limit:email_list.limit,
                totalCount:email_list.emails_count,
            });
            if($("#pages").html()) $(".page_select").removeClass('hidden');
            $("#pages > ul > li").click(function(){
                var page = $("#pages .active").text();
                email_list.get_page_emails(page);
            });
            $.unblockUI();
        });

    },

    get_page_emails:function(page){
        var paras = {};
        paras.page = page;
        paras.limit = email_list.limit;
        $.postJSON1('/emails/j',paras,function(o){
            email_list.emails = o.emails;
        })

    },

    changeLimit:function(){
         email_list.get_emails();
    },

    goPage:function(){
        var page = $("#go-page").val();
        $("#go-page").val('');
        $("#page_"+page).click();
    },

    }
);


var email_new = avalon.define({
    $id: 'email_new',
    e_model: {
        _id: 0,
        content: ''
    },

    e_models: [
        {
            _id: 0,
            content: ''
        }
    ],

    email: {
        subject: '',
        receiver:'',
        message: '',
        model_id: '0'
    },

    offers: [{}],

    e_model_change: function(e){
        $.postJSON1("/j/e_model", {'content': {'e_model_id': e.target.value}, 'action': 'query'}, function (o) {
            if (!o.err) {
                email_new.e_model = o.e_model;
                email_new.email.message = o.e_model.content;
            }
        });
    },

    send: function(){
        var o = {"action": "send", "content": email_new.email}
        $.postJSON1("/j/email", o, function(o) {
            if (!o.err) {
                location.href = "/email";
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

    get_offers: function() {
        $.getJSON1("/j/email/offers", {}, function (o) {
            if (!o.err) {
                email_new.offers = o.offers;
            }
        });
    },

    get_affiliate_emails: function(offer_ids){
        var data = {'offer_ids': offer_ids}
        $.getJSON1("/j/email/affiliate_email", data, function (o) {
            if (!o.err) {
                email_new.email.receiver = o.affiliate_emails.join();
            }
        });
    },
});




var email_models = avalon.define({
    $id: 'e_models',
    models: [
            {
                _id: '1',
                model_name: '',
                content: '',
                createdTime: ''
            }
        ],

    model: {
         _id: '1',
        model_name: '',
        content: '',
        createdTime: ''
    },

    totalPage:'', 
    limit:$("#display").val(),
    models_count:'',


    save: function(){
        var o = {"action": "create", "content": email_models.model}
        $.postJSON1("/j/e_model", o, function(o) {
            if (!o.err) {
                location.reload();
            }
        });
    },
    edit_e_model: function(model){
        email_models.model = model;
    },

    delete_e_model: function(model){
        var content = {
            'e_model_id': model._id,
        };
        var o = {"action": "delete", "content": content};
        $.postJSON1("/j/e_model", o, function(o) {
            if (!o.err) {
                email_models.get_models();
                if(!$("#pages").html()) $(".page_select").addClass('hidden');
            }
        });
    },


    update: function(){
        var content = {
            'e_model_id': email_models.model._id,
            'content': email_models.model.content,
            'model_name': email_models.model.model_name
        }
        var o = {"action": "update", "content": content};
        $.postJSON1("/j/e_model", o, function(o) {
            if (!o.err) {
                location.reload();
            }
        });
    },


    get_models:function(){
        $.blockUI({
            css:{top:"40px"},
        });
        var paras = {};
        paras.page = '1';
        paras.limit = email_models.limit; 
        $.postJSON1('/e_model/j',paras,function(o){
            email_models.models = o.models;
            email_models.models_count = o.models_count;
            email_models.totalPage = Math.ceil(email_models.models_count/email_models.limit)
            $("#pages").extendPagination({
                limit:email_models.limit,
                totalCount:email_models.models_count,
            });
            if($("#pages").html()) $(".page_select").removeClass('hidden');
            $("#pages > ul > li").click(function(){
                var page = $("#pages .active").text();
                email_models.get_page_models(page);
            });
            $.unblockUI();
        });

    },

    get_page_models:function(page){
        var paras = {};
        paras.page = page;
        paras.limit = email_models.limit;
        $.postJSON1('/e_model/j',paras,function(o){
            email_models.models = o.models;
        })

    },

    changeLimit:function(){
        email_models.get_models();
    },

    goPage:function(){
        var page = $("#go-page").val();
        $("#go-page").val('');
        $("#page_"+page).click();
    },    
});