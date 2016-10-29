var NetWork = avalon.define({
    $id: 'network',
    networks: [
        {
            name: 'Facebook',
            ad_count: '1',
            ads: [
                {
                    units: 'Banner',
                    format: 'Banner',
                    slot_id: '1',
                    placement: '1234',
                    is_auth: true,
                    is_paused: false,
                },
            ],
            sdk: [{
                doc_link: 'http://baidu.com',
                sdk_link: 'http://google.com'
            }],
            adapter: 'http://bing.com',
            auth_manager: '',
            login_auth_args: []
        }
    ],

    save: function(){
        var network_name = $("#network_name").val();
        var network_adapter = $("#network_adapter").val();
        var network_auth_code = $("#network_auth_code").val();
        var network_auth_name = $("#network_auth_name").val();
        var network_auth_token = $("#network_auth_token").val();
        var sdk = []
        $(".sdk").each(function(){
            var _sdk = {
                'platform': $(".sdk_platform", $(this)).val(),
                'doc_link': $(".doc_link", $(this)).val(),
                'sdk_link': $(".sdk_link", $(this)).val()
            };
            sdk.push(_sdk)
        })
        
        data = {
            name: network_name,
            adapter: network_adapter,
            auth_manager: {'auth_name': network_auth_name, 'auth_code': network_auth_code, 'auth_token': network_auth_token},
            sdk: sdk,
            auth: '',
        }

        $.postJSON1('/network/create', data, function(o){
            if(!o.err){
                location.href = '/network'
            }else{
                $(".err").remove();
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("."+k).after('<div class="err">'+v+"</div>")
                }
            }
        })
    },

    cancel_network: function(){
        $("#add_info").html('');
    },

    pull_push: function(net_name){
        var _tbody = $(this).parent().parent().parent();
        if($(".pull_push", $(this)).hasClass("glyphicon-triangle-right")){
            $(".pull_push", $(this)).attr('class', 'pull_push glyphicon glyphicon-triangle-bottom');
            $(".ads_tr", _tbody).css("display", "");
        }else{
            $(".pull_push", $(this)).attr('class', 'pull_push glyphicon glyphicon-triangle-right');
            $(".ads_tr", _tbody).css("display", "none");
        }
    },

    edit_network: function(network){
        NetWorkAuthCode.network.name = network.name;
        NetWorkAuthCode.network._id = network._id;
        var auth_manager = network.auth_manager;
        var auth_manager_list = [];
        if(auth_manager == ''){
            auth_manager = network.login_auth_args;
            for(var i=0; i < auth_manager.length; i++){
                var _a_m = [auth_manager[i], '']
                auth_manager_list.push(_a_m);
            }
        }else{
            auth_manager = auth_manager.split(";")
            for(var i=0; i < auth_manager.length; i++){
                var _a_m = auth_manager[i].split('=');
                if(_a_m[0] != ''){
                    auth_manager_list.push(_a_m);
                }
            }
        }

        NetWorkAuthCode.network.auth_manager = auth_manager_list;

    },
})

var NetWorkAuthCode;
NetWorkAuthCode = avalon.define({
    $id: 'AuthCode',
    network: {
        _id: '',
        name: '',
        auth_manager: []

    },

    edit_network: function(){
        var args = '';
        for(var i=0; i<NetWorkAuthCode.network.auth_manager.length; i++){
            var arg = NetWorkAuthCode.network.auth_manager.$model[i][0];
            if(arg != undefined){
                var value = $("#"+arg).val();
                arg = arg + '=' + value + ';'
                args += arg;
            }
        };
        NetWorkAuthCode.network.auth_manager = args;
        $.postJSON1('/network/update', NetWorkAuthCode.network, function(o){
            if(!o.err){
                location.reload();
            }else{
                $(".err").remove();
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("."+k).after('<div class="err">'+v+"</div>")
                }
            }
        })
    }
})

$(function(){
    $("#network_btn1").click(function(){
            $("#network_btn1 h4").addClass("network_active");
            $("#network_btn2 h4").removeClass("network_active");
            $("#netWork_page1").show();
            $("#netWork_page2").hide();
            $("#button_add").show();
            }
    );
    $("#network_btn2").click(function(){
            $("#network_btn2 h4").addClass("network_active");
            $("#network_btn1 h4").removeClass("network_active");
            $("#netWork_page2").show();
            $("#netWork_page1").hide();
            $("#button_add").hide();
            }
    );
    $("#add_con").click(function(){
        var html = [
            '<div class="row add_model sdk">',
            '<div class="col-xs-2">platform :</div>',
            '<div class="col-xs-2">',
            '<select class="sdk_platform"><option value="Android">Android</option><option value="Ios">IOS</option></select></div>',
            '<div class="col-xs-2">doc_link :</div>',
            '<div class="col-xs-2"><input class="doc_link" type="text" value=""></div>',
            '<div class="col-xs-2">sdk_link :</div>',
            '<div class="col-xs-2"><input class="sdk_link" type="text" value=""></div></div>'
        ].join("")
        $("#add_info").append(html);
    });
});
