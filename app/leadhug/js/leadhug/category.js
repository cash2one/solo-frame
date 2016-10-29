var category = avalon.define(
    {
        $id:'category',
        status: '0',
        cat:[
            {}
        ],

        limit: $("#display").val(),
        totalPage: '',
        cat_count:'',


        filter: function(){
            category.get_category();
                
        },
  


        get_category:function(){
            $.blockUI({
                css:{top:"40px"},
            });
            var paras = {};
            paras.page = '1';
            paras.limit = category.limit;
            paras.status = category.status; 
            $.postJSON1('/category/manage',paras,function(o){
                category.cat = o.cat;
                category.cat_count = o.cat_count;
                category.totalPage = Math.ceil(category.cat_count/category.limit);
                $("#pages").extendPagination({
                    limit:category.limit,
                    totalCount:category.cat_count,
                });
                if($("#pages").html()) $(".page_select").removeClass('hidden');
                $("#pages > ul > li").click(function(){
                    var page = $("#pages .active").text();
                    category.get_page_category(page);
                });
                $.unblockUI();
            }); 

        },  

        get_page_category:function(page){
            var paras = {};
            paras.page = page;
            paras.limit = category.limit;
            $.postJSON1('/category/manage',paras,function(o){
                category.cat = o.cat;
            })  

        },

        changeLimit:function(){
            category.get_category();
        },  
        goPage:function(){
            var page = $("#go-page").val();
            $("#go-page").val('');
            $("#page_"+page).click();
        },    

/*        filter: function(){
            var url = '/category/manage?status='+category.status;
            $.getJSON1(url, {}, function(o) {
                 if (!o.err) {
                    category.cat= o.cat
                }
            });
        },
*/
        filter: function(){
            category.get_category();
                
        },
  


        get_category:function(){
            $.blockUI({
                css:{top:"40px"},
            });
            var paras = {};
            paras.page = '1';
            paras.limit = category.limit;
            paras.status = category.status; 
            $.postJSON1('/category/manage',paras,function(o){
                category.cat = o.cat;
                category.cat_count = o.cat_count;
                category.totalPage = Math.ceil(category.cat_count/category.limit);
                $("#pages").extendPagination({
                    limit:category.limit,
                    totalCount:category.cat_count,
                });
                if($("#pages").html()) $(".page_select").removeClass('hidden');
                $("#pages > ul > li").click(function(){
                    var page = $("#pages .active").text();
                    category.get_page_category(page);
                });
                $.unblockUI();
            }); 

        },  

        get_page_category:function(page){
            var paras = {};
            paras.page = page;
            paras.limit = category.limit;
            $.postJSON1('/category/manage',paras,function(o){
                category.cat = o.cat;
            })  

        },

        changeLimit:function(){
            category.get_category();
        },  
        goPage:function(){
            var page = $("#go-page").val();
            $("#go-page").val('');
            $("#page_"+page).click();
        },    



    }
)


var category_modify = avalon.define(
    {
        $id:'category_modify',
        category: {
            _id: '',
            name: '',
            status: '1'
        },

        err: '',

        save: function(){
            var url = '/category/modify/'+category_modify.category._id;
             $.postJSON1(url, category_modify.category, function(o) {
                 if (!o.err) {
                        location.href = '/category/manage'
                 }else{
                     category_modify.err = o.err;
                 }
            });
        }
    }
)