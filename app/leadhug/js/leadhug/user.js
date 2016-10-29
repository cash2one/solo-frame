var user_list;
user_list = avalon.define(
    {
        $id: 'user_list',
        users: [
            {
                _id: '',
                account: '',
                email: '',
                role: {
                    name: ''
                },
                createdTime: ''
            }
        ],

        user: {
            _id: '',
            account: '',
            password: '',
            email: '',
            skype_id: '',
            phone: '',
            role_id: ''
        },

        edit_user: {
            _id: '',
            account: '',
            password: '',
            email: '',
            skype_id: '',
            phone: '',
            role_id: ''
        },

        roles: [
            {
                _id: '',
                name: ''
            }
        ],

        limit:$("#display").val(),
        totalPage:'',
        users_count:'',

        get_roles: function () {
            $.getJSON1("/j/roles", {}, function (o) {
                if (!o.err) {
                    user_list.roles = o.roles;
                }
            });
        },

        user_create: function(){

        },

        save: function (){
            $.postJSON1("/j/user/new", user_list.user, function (o) {
                if (!o.err) {
                    location.reload();
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

        user_update: function(){
            var content = {
                '_id': user_list.edit_user._id,
                'account': user_list.edit_user.account,
                'email': user_list.edit_user.email,
                'password': user_list.edit_user.password,
                'role_id': user_list.edit_user.role_id,
                'skype_id': user_list.edit_user.skype_id,
                'phone': user_list.edit_user.phone
            }
            $.postJSON1("/j/user/update", content, function (o) {
                if (!o.err) {
                    location.reload();
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

        user_delete: function (obj) {
            $.postJSON1("/j/user/delete", {"user_id": obj._id}, function (o) {
                if (!o.err) {
                    //user_list.users.remove(obj);
                    window.location.reload();
                }else{
                    console.log(o.err);
                };
            });
        },

        user_edit: function (obj) {
            user_list.edit_user = obj;
        },



        get_users:function(){
            $.blockUI({
                css:{top:"40px"},
            });
            var paras = {};
            paras.limit = user_list.limit;
            paras.page = '1';
            $.postJSON1('/j/user/manage',paras,function(o){
                    user_list.users = o.users;
                    user_list.users_count = o.users_count;
                    user_list.totalPage = Math.ceil(o.users_count/user_list.limit);
                    $("#pages").extendPagination({
                        totalCount:user_list.users_count,
                        limit:user_list.limit,
                    });
                    if($("#pages").html()) $(".page_select").removeClass('hidden');
                    $("#pages > ul > li").click(function(){
                        page = $("#pages .active").text();
                        user_list.get_page_users(page);
                    });
            });
            $.unblockUI();
        },

        get_page_users:function(page){
            var paras = {};
            paras.limit = user_list.limit;
            paras.page = page;
            $.postJSON1('/j/user/manage',paras,function(o){
                user_list.users = o.users;
            });
        },

        changeLimit:function(){
            user_list.get_users();
        },

        goPage:function(){
            var page = $("#go-page").val();
            $("#go-page").val('');
            $("#page_" + page).click();
        },
    }
);
