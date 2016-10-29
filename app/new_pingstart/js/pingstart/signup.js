var model = avalon.define({
    $id: "register",
    captcha_img: "data:image/jpg;base64,",
    o:{
    captcha_key: "",
    captcha_code: "",
    email: "",
    password: "",
    password2: "",
    company: "",
    },
    signup: function(){
        $.postJSON1(
            "/j/signup",
            avalon.vmodels.register.o.$model,
            function(o){
                $('.err').remove()
                if (o.err) {
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("#"+k).after('<div class="err">'+v+"</div>")
                    }
                    avalon.vmodels.register.get_captcha();
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
                avalon.vmodels.register.o.captcha_key=o.key;
                avalon.vmodels.register.captcha_img="data:image/jpg;base64," + o.img;
            }
        )
    }
})
avalon.ready(
    function(){
        avalon.vmodels.register.get_captcha();
        $("body").keypress(
           function(e){
               if(e.which == 13){
                    $("#btn_login").click();
               }
           }
       )
    }
)