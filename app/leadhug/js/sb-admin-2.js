$(function() {

    $('#side-menu').metisMenu();
    //$(".operate_close").click(function(){
    //    location.reload();
    //})

});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    $(window).bind("load resize", function() {
        topOffset = 50;
        width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    });

    var url = window.location;
    var element = $('ul.nav a').filter(function() {
        return this.href == url || url.href.indexOf(this.href) == 0;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }
});

var model = avalon.define({
    $id: 'base',
    old_password: '',
    verify: '',
    old_verify_status: false,
    new_password: '',
    new_password_verify: '',
    new_verify_status: false,
    confirm_password: '',
    confirm_verify: '',
    confirm_verify_status: false,

    verify_old_password: function(e){
        $.postJSON1("/j/password/verify", {'password': model.old_password}, function(o) {
            if (o.res) {
                model.verify = o.res,
                model.old_verify_status = true;
            }
        });
    },

    verify_new_password: function(e){
        $.postJSON1("/j/new_password/verify", {'password': model.new_password}, function(o) {
            if (o.res) {
                model.new_password_verify = o.res;
                model.new_verify_status = true;
            }
        });
    },

    verify_confirm_password: function(e){
        var obj = {'new_password': model.new_password, 'confirm_password': model.confirm_password}
        $.postJSON1("/j/password_confirm/verify", obj, function(o) {
            if (o.res) {
                model.confirm_verify = o.res;
                model.confirm_verify_status = true;
            }
        });
    },

    save_password: function(){
        if(model.old_verify_status && model.new_verify_status && model.confirm_verify_status){
            var obj = {'new_password': model.new_password}
            $.postJSON1("/j/password/modify", obj, function(o) {
            if (!o.err) {
                    location.reload();
                }
            });
        }else{
            return;
        }
    }
})
