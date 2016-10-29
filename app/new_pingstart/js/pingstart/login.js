var model = avalon.define({
    $id: "login",
    captcha_img: "data:image/jpg;base64,",
    o:{
    captcha_key: "",
    captcha_code: "",
    email: "",
    password: "",
    },
    login: function(){
        $.postJSON1(
            "/j/login",
            avalon.vmodels.login.o.$model,
            function(o){
                $('.err').remove()
                if (o.err) {
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("#"+k).after('<div class="err">'+v+"</div>")
                    }
                    avalon.vmodels.login.get_captcha();
                } else {
                    location.href = "/";
                }
            }
        )
    },
    get_captcha: function(){
        $.getJSON(
            "/j/captcha",
            function(o){
                avalon.vmodels.login.o.captcha_key=o.key;
                avalon.vmodels.login.captcha_img="data:image/jpg;base64," + o.img;
            }
        )
    },

    forget_password: function(){
        $('.err').remove();
        if(!model.o.email){
            $("#email").after('<div class="err">email cat\'t be empty!</div>');
            return;
        }

        $.postJSON1("/j/email_verify", {'email': model.o.email},
            function(o){
                if (!o.signup) {
                    $("#email").after('<div class="err">The email not Sign Up!</div>');
                    return;
                } else {
                    location.href = "/find_password?email=" + model.o.email;
                }
            }
        )

    }
})
avalon.ready(
    function(){
        avalon.vmodels.login.get_captcha();
        $("body").keypress(
           function(e){
               if(e.which == 13){
                    $("#btn_login").click();
               }
           }
           ) 
    }
)
