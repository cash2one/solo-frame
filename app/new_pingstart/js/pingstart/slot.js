var Slot = avalon.define({
    $id: 'slot',
    slots: [
        {
            _id: 1,
            name: 'facebook',
            slot_type: 'Facebook',
            last_operated: '2016-04-11',
        }
    ],

    slots_count: '',
    limit: 10,

    new_slot: {
        name: '',
        slotType: ''
    },

    search_query: {
        name: '',
    },
    slot_status:function(slot_id){
        data = {
            "slot_id":slot_id,
        };
        $.postJSON1("/slot/status",data, function(o){
            if (!o.err) {
                    location.reload();
                }
        }
        );
    },
    save: function(){
        $.postJSON1("/slot/create", Slot.new_slot, function (o) {
                if (!o.err) {
                    location.reload();
                }else{
                    $(".err").remove();
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("."+k).after('<div class="err err_pl">'+v+"</div>")
                    }
                };
            });
    },
    slot_delete: function(id) {
       if (!confirm("确认要删除？")) {
                window.event.returnValue = false;
            }
        else{
            $.postJSON1("/slot/delete/"+id, {}, function (o) {
            location.reload()
        })
        }
    },
    get_slots: function(){
        var data = {
            page: 1,
            limit: Slot.limit,
            name: Slot.search_query.name
        };
        $.getJSON1("/slots", data, function (o) {
            Slot.slots = o.slots;
            Slot.slots_count = o.slots_count;
            $("#pages").extendPagination({
                totalCount: Slot.slots_count,
                limit: Slot.limit
            });
            $("#pages > ul > li").click(function(){
                var page = $("#pages .active").text();
                Slot.get_page_slots(page);
            })
        })
    },

    get_page_slots: function(page){
        $.getJSON1("/slots", {'page': page, 'limit': Slot.limit}, function (o) {
            Slot.slots = o.slots;
        })
    }
})


var SlotEdit;
SlotEdit = avalon.define({
    $id: 'slot_edit',
    slot: {
        _id: '',
        name: '',
        slotType: '',
        network_select: [
            {
                _id: '',
                name: ''
            }
        ],

        bind_networks: [
            {
                network_id: '',
                network_name: '',
                placement_id: {},
                is_auth: false,
                auth_code: '',
                is_paused: false,
                priority: '',
            }
        ],
        model: {
        'app':true,
        'other':true
        },
        appBlackList:''
    },

    network_add: {
        network_id: '',
        network_name: '',
        placement_id: '',
        is_auth: false,
        is_paused: false,
        priority: '',
        auth_manager: ''
    },

    placement_id: [],
    auth_manager_args: [],

    network_add_auth: {
        network_id: '',
        auth_manager: '',
        login_auth_args: [],
    },

    network_is_exist: false,
    select_network: function (e) {
        var value = e.target.value.split('*');
        SlotEdit.network_add.is_auth = false;
        if(value[0] == ''){
            $(".auth_info").css("display", "none");
            SlotEdit.placement_id = [];
            $("#is_auth").attr('disabled', true);
            return;
        };
        $("#is_auth").attr('disabled', false);
        SlotEdit.network_add.network_id = value[0]
        SlotEdit.network_add.network_name = value[1]
        SlotEdit.network_add_auth.network_id = value[0]
        SlotEdit.network_add_auth.auth_manager = value[2]
        SlotEdit.network_add_auth.login_auth_args = value[4]
        SlotEdit.display_arg_id();
        SlotEdit.placement_id = value[3].split(',')
        var err;
        SlotEdit.network_is_exist = false;
        SlotEdit.slot.bind_networks.forEach(function (item, index) {
            if (item.network_id == value[0]) {
                SlotEdit.network_is_exist = true;
                err = '<div class="err" style="margin-left: 300px;">The NetWork is Existed</div>';
            }
        });
        $(".err").remove();
        if(SlotEdit.network_is_exist){
            $("#network").after(err);
            return;
        }
    },

    display_arg_id: function(){
        var auth_manager = SlotEdit.network_add_auth.auth_manager,
                    auth_manager_list = [];
                if(auth_manager == ''){
                    auth_manager = SlotEdit.network_add_auth.login_auth_args.split(",");
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
                SlotEdit.auth_manager_args = auth_manager_list;
    },

    add_network: function () {
        if($(".err").length >= 1)return;
        var _auth_manager = SlotEdit.network_add_auth.auth_manager;
        if(SlotEdit.network_add.is_auth){
            _auth_manager = SlotEdit.add_auth();
        }
        SlotEdit.network_add.auth_manager = _auth_manager;
        SlotEdit.network_add.priority = SlotEdit.slot.bind_networks.length;
        var args = '';
        for(var i=0; i<SlotEdit.placement_id.length; i++){
            var arg = SlotEdit.placement_id.$model[i];
            if(arg != undefined){
                var value = $("#"+arg).val();
                arg = arg + '=' + value + ';'
                args += arg;
            }
        };
        SlotEdit.network_add.placement_id = args;
        var add_network = JSON.parse(JSON.stringify(SlotEdit.network_add));
        SlotEdit.network_is_exist = false;
        var err;
        if(SlotEdit.network_add.network_id==''){
            SlotEdit.network_is_exist = true;
            err = '<div class="err" style="margin-left: 300px;">The NetWork cat\'t be empty!</div>'
        };

        SlotEdit.slot.bind_networks.forEach(function (item, index) {
            if (item.network_id == add_network.network_id) {
                SlotEdit.network_is_exist = true;
                err = '<div class="err" style="margin-left: 300px;">The NetWork is Existed</div>';
            }
        });
        $(".err").remove();
        if(SlotEdit.network_is_exist){
            $("#network").after(err);
            return;
        }
        $('.auth_info').css('display', 'none');
        $("#is_auth").attr("disabled", true);
        SlotEdit.slot.bind_networks.push(add_network);
        $("#select_network").val("");
        SlotEdit.network_add.placement_id = '';
        SlotEdit.network_add.is_auth = false;
        SlotEdit.placement_id = [];
        SlotEdit.network_add.auth_manager = '';

    },

    delete_network: function (network) {
        $(".err").remove();
        SlotEdit.slot.bind_networks.remove(network);
        SlotEdit.slot.bind_networks.forEach(function (item, index) {
            item.priority = index;
        })
    },

    paused_or_open: function (network) {
        var _this = $(this)
        if($("#on_off", _this).hasClass("glyphicon-pause")){
            network.is_paused = false;
        }else if($("#on_off", _this).hasClass("glyphicon-open")){
            network.is_paused = true;
        }

    },

    priority_asc: function (network) {
        var _index = SlotEdit.slot.bind_networks.indexOf(network);
        if (!_index)return;
        network.priority--;
        SlotEdit.slot.bind_networks[_index - 1].priority++;
        var _network = network;
        SlotEdit.slot.bind_networks.remove(network)
        SlotEdit.slot.bind_networks.splice((_index - 1), 0, _network);
    },

    save: function(){
        if(document.getElementById("slotedit41").checked == false && document.getElementById("slotedit42").checked ==false){
            alert("请选Ad Categories中至少一种")
        }else{
        var network = [];
        SlotEdit.slot.bind_networks.forEach(function(el, i){
            var obj_tmp = {
                network_id: el.network_id,
                network_name: el.network_name,
                placement_id: el.placement_id,
                is_auth: el.is_auth,
                is_paused: el.is_paused,
                priority: el.priority,
                auth_manager: el.auth_manager
            };
            network.push(obj_tmp);
        });
        var data = {
            slot_id: SlotEdit.slot._id,
            slot_name: SlotEdit.slot.name,
            network: network,
            model: SlotEdit.slot.model,
            appBlackList:SlotEdit.slot.appBlackList

        }
        $.postJSON1("/slot/update", data, function (o) {
            if(!o.err){
                location.href='/slot'
            }else{
                $(".err").remove();
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("."+k).after('<div class="err" style="margin-left: 300px;">'+v+"</div>")
                }
            }
        })
        }
    },

    is_auth_fun: function(e){
        if(SlotEdit.network_add.is_auth){
            $('.auth_info').css('display', '');
        }else{
            $('.auth_info').css('display', 'none');
        }
    },

    add_auth: function(){
        var auth_manager_args = SlotEdit.auth_manager_args;
        var args = '';
        for(var i=0; i < auth_manager_args.length; i++){
            var arg = auth_manager_args[i][0],
                value = auth_manager_args[i][1]
            arg = arg + '=' + value + ';'
            args += arg;
        };
        return args;
    },

    placement_change: function(){
        var args = '';
        for(var i=0; i<SlotEdit.placement_id.length; i++){
            var arg = SlotEdit.placement_id.$model[i];
            if(arg != undefined){
                var value = $("#"+arg).val();
                arg = arg + '=' + value + ';'
                args += arg;
            }
        };
        SlotEdit.network_add.placement_id = args;
        $.postJSON1("/placement_id/verify", SlotEdit.network_add, function (o) {
            if(o.err){
                $(".err").remove();
                    for (k in o.err) {
                        var v;
                        v = o.err[k];
                        $("#"+k).after('<div class="err" style="margin-left: 300px;">'+v+"</div>")
                }
            }
        })
    }
});

$(function(){
    $("#btn_apps").click(function(){
        $(this).addClass("color_bg");
        $("#btn_keywords").removeClass("color_bg");
        $("#keywords").addClass("disappear");
        $("#apps").removeClass("disappear");
    });
    $("#btn_keywords").click(function(){
        $(this).addClass("color_bg");
        $("#btn_apps").removeClass("color_bg");
        $("#apps").addClass("disappear");
        $("#keywords").removeClass("disappear");
    });
    $("#slotedit41").click(function(){
        if(document.getElementById("slotedit41").checked == false && document.getElementById("slotedit42").checked ==false){
            alert("请至少选择其中一种")
        }
   });
   $("#slotedit42").click(function(){
        if(document.getElementById("slotedit41").checked == false && document.getElementById("slotedit42").checked ==false){
            alert("请至少选择其中一种")
        }
   })
});


