var post_back = avalon.define({
    $id: 'post_back',
    add: false,
    edit: false,

    post_backs: [
        {
            _id: '',
            url: ''
        }
    ],

    add_url: '',
    local_storage:[{}],
    selected:$("#display").val(),
    totalPage:'',

/*    GetPostBacks: function(){
        $.getJSON1("/post_backs", {}, function(o) {
                post_back.post_backs = o.post_backs;
        });
    },*/

    GetPostBacks: function(){
        $.getJSON1("/post_backs", {}, function(o) {
                post_back.local_storage = o.post_backs;
                post_back.pager(post_back.local_storage);
                var limit = post_back.selected;
                to_show = post_back.local_storage.slice(0,limit);
                post_back.post_backs = to_show;
        });
    },

    changeLimit:function(){
        var data = post_back.local_storage;  //all the mails
        var limit = post_back.selected;     //limitation to show
        post_back.pager(data);     //re-pager according to the new limitation
        post_back.post_backs = data.slice(0,limit);  //re-show the emails on 1st page
    },

    pager:function(o){
        var length = o.length  //a
        var limit = post_back.selected;     //limitation to show
        post_back.totalPage = Math.ceil(length/Number(limit));
        $("#pages").extendPagination({                       //a framework
            totalCount:length,
            limit:limit,
        });
        if($("#pages").html()) $(".page_select").removeClass('hidden');
        $("#pages > ul > li").click(function(){               //bond every page with a click event
            page = $("#pages .active").text();
           post_back.change_page(page);
        });
    },

    change_page:function(page){
        var data = post_back.local_storage;  //all the mails
        var limit = post_back.selected;     //limitation to show
        var to_show = data.slice((page-1)*limit,page*limit); //pick content on specific page out
        post_back.post_backs = to_show;         //show the content
    },

    goPage:function(){
        var page = $("#go-page").val();
        $("#go-page").val('');
        $("#page_"+page).click();
    },


    Save: function(){
        $.postJSON1("/post_back/create", {'url': post_back.add_url}, function(o) {
            if (!o.err) {
                location.reload();
            }
        });
    },

    Add: function(){
        post_back.add = true;
    },

    Cancel: function(){
        post_back.add = false;
        post_back.add_url = '';
    },

    Edit: function(_id){
        $("#"+_id + " span").css('display', 'none');
        $("#"+_id + " input").css('display', '');
        $("#edit_"+_id).css('display', 'none');
        $("#update_"+_id).css('display', '');

    },

    Update: function(obj){
        $.postJSON1("/post_back/update", {'_id': obj._id, 'url': obj.url}, function(o) {
            if (!o.err) {
                location.reload();
            }
        });
    },

    CancelEdit: function(_id){
        $("#"+_id + " span").css('display', '');
        $("#"+_id + " input").css('display', 'none');
        $("#edit_"+_id).css('display', '');
        $("#update_"+_id).css('display', 'none');
    },

    Delete: function(obj){
        $.postJSON1("/post_back/delete", {'_id': obj._id}, function(o) {
                 if (!o.err) {
                    var page = $("#pages .active").text();
                    if($("#pages .next").prev().prev().text() == page){
                        post_back.local_storage.remove(obj);  //here
                        post_back.pager(post_back.local_storage); //here
                        if(post_back.local_storage.length == 0){window.location.reload();};
                        if($("#pages .next").prev().prev().text() != page){page=Number(page)-1};
                        $("#page_"+page).click();
                    }else{
                        post_back.local_storage.remove(obj);  //here
                        post_back.pager(post_back.local_storage); //here
                        if(post_back.local_storage.length == 0){window.location.reload();};
                        $("#page_"+page).click();};
                 }
        });
    }
});

avalon.ready(
    function(){
        avalon.vmodels.post_back.GetPostBacks();
    }
)
