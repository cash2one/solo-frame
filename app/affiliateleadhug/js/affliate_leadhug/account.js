var Account=avalon.define({
    $id: 'account',
    captcha_img: '',

    account: {
        captcha_key: "",
        captcha_code: "",
        account: '',
        email: '',
        password: '',
        confirmPassword: '',
        skype_id: '',
        phone: '',
        country: '',
        company: '',
    },

    get_captcha: function(){
        $.getJSON(
            "/j/captcha",
            function(o){
                avalon.vmodels.account.account.captcha_key=o.key;
                avalon.vmodels.account.captcha_img="data:image/jpg;base64," + o.img;
            }
        )
    },

    sign: function(){
        $.postJSON1(
            "/j/sign",
            avalon.vmodels.account.account.$model,
            function(o){
                $('.err').remove()
                if (o.err) {
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("#"+k).after('<div class="err" style="color: red">'+v+"</div>")
                    }
                    avalon.vmodels.account.get_captcha();
                } else {
                    //location.href = "/";
                    $(".btn-signup").css('display', 'none');
                    $('#sign_success').css('display', 'block')
                }
            }
        )
    }
})

var Account_info=avalon.define({
    $id:'account_info',
    affiliate_info:{
        name: '',
        email:'',
        country:'',
        password:'',
        phone:'',
        skype_id:'',
        company:'',
        payment: {
                invoice_frequency: '',
                threshold: '',
                payment_method: '',
                beneficiary: '',
                account_number:'',
                bank: '',
                route:'',
                paypal:''
            },
    err:''


    },
    save:function(){
        var url = '/j/account/save'
        $.postJSON1(url, Account_info.affiliate_info, function(o) {
            if (!o.err) {
                    location.href = '/account'
                }
            else {
                $(".err").remove();
                    console.log(o.err)
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("."+k).after('<div class="err" style="color: red">'+v+"</div>")
                    }
            }
        });
    }
})

avalon.ready(
    function(){
        avalon.vmodels.account.get_captcha();
    }
)
