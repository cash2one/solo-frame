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
                        $("#"+k).after('<div class="err" style="color: red">'+v+"</div>")
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
    }
})
avalon.ready(
    function(){
        avalon.vmodels.login.get_captcha();
    }
)
