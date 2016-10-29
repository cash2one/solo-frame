var modify_password;
modify_password = avalon.define({
    $id: 'modify_password',

    old_password: '',
    new_password: '',
    confirm_password: '',

    old_passwd_ok: false,
    new_passwd_ok: false,
    confirm_passwd_ok: false,
    old_password_verify: function(){
        $.postJSON1("/old_password_verify", {'old_password': modify_password.old_password}, function (o) {
            $(".err").remove();
            if(o.err){
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("#"+k).after('<div class="err" style="margin-left: 115px;">'+v+"</div>")
                }
            }else{
                modify_password.old_passwd_ok = true;
            }
        })
    },

    verify_password: function(){
        $.postJSON1("/verify_password", {'new_password': modify_password.new_password}, function (o) {
            $(".err").remove();
            if(o.err){
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("#"+k).after('<div class="err" style="margin-left: 115px;">'+v+"</div>")
                }
            }else{
                modify_password.new_passwd_ok = true;
                modify_password.verify_confirm();
            }
        })
    },

    verify_confirm: function () {
        var data = {
            'new_password': modify_password.new_password,
            'confirm_password': modify_password.confirm_password
        }
        $.postJSON1("/verify_confirm", data, function (o) {
            $(".err").remove();
            if(o.err){
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("#"+k).after('<div class="err" style="margin-left: 115px;">'+v+"</div>")
                }
            }else{
                modify_password.confirm_passwd_ok = true;
            }
        })
    },

    modify_password: function(){
        if(!modify_password.old_passwd_ok || !modify_password.new_passwd_ok || !modify_password.confirm_passwd_ok)return;
        var data = {
            password: modify_password.confirm_password
        }
        $.postJSON1("/modify_password", data, function (o) {
            alert("modify password successful!");
            $(".modify_password_cancel").click();
            modify_password.old_password = '',
            modify_password.new_password = '',
            modify_password.confirm_password = ''
        })
    },

    cancel: function(){
            $(".err").remove();
            modify_password.old_password = '',
            modify_password.new_password = '',
            modify_password.confirm_password = ''
    }
})
