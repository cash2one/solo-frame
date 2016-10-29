var ForgetPassword;
ForgetPassword = avalon.define({
    $id: 'forget_password',
    email: '',
    captcha_code: '',
    new_password: '',
    confirm_password: '',
    new_passwd_ok: false,
    confirm_passwd_ok: false,

    send_captcha: function(email){
        $.postJSON1("/send_captcha", {'email': ForgetPassword.email}, function (o) {

        })
    },

    verify_captcha: function(){
        $.postJSON1("/verify_captcha", {'email': ForgetPassword.email, 'captcha_code': ForgetPassword.captcha_code}, function (o) {
            $(".err").remove();
            if(!o.err){
                $(".reset_password").css("display", "");
            }else{
                $("#captcha_code").after('<div class="err" style="margin-left: 140px;margin-top: 10px;">'+ o.err.captcha_code +'</div>')
            }
        })
    },

    verify_password: function(){
        $.postJSON1("/verify_password", {'new_password': ForgetPassword.new_password}, function (o) {
            $(".err").remove();
            if(o.err){
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("#"+k).after('<div class="err" style="margin-left: 140px;margin-top: 10px;">'+v+"</div>")
                }
            }else{
                ForgetPassword.new_passwd_ok = true;
                ForgetPassword.verify_confirm();
            }
        })
    },

    verify_confirm: function () {
        var data = {
            'new_password': ForgetPassword.new_password,
            'confirm_password': ForgetPassword.confirm_password
        }
        $.postJSON1("/verify_confirm", data, function (o) {
            $(".err").remove();
            if(o.err){
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("#"+k).after('<div class="err" style="margin-left: 140px;margin-top: 10px;">'+v+"</div>")
                }
            }else{
                ForgetPassword.confirm_passwd_ok = true;
            }
        })
    },

    reset_password: function(){
        if(!ForgetPassword.new_passwd_ok || !ForgetPassword.confirm_passwd_ok)return;
        var data = {
            email: ForgetPassword.email,
            password: ForgetPassword.confirm_password
        }
        $.postJSON1("/reset_password", data, function (o) {
            location.href = '/login'
        })
    }
})
