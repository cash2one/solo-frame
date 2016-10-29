(function($){
    var editer = function(container,params){
        var flag = 0;
        $(document).on('click',container+' td a.edit',function(){
        	change($(this));
        });
        $(document).on('click',container+' td a.cancel',function(){
        	cancel($(this));
        });
        $(document).on('click',container+' td a.delete',function(){
            remove($(this));
        });
        $(document).on('click',container+' td a.submit',function(){
            submit($(this));
        });
        change = function($elem){
             $td = $elem.parent().prev();
             $td.append('<input value="'+$td.children('span').text()+'">');
        	 $td.children('span').hide();
        	 $elem.parent().append('<a class="submit btn btn-primary btn-xs">save</a><a class="cancel btn btn-xs">cancel</a>');
        	 $elem.next().hide();
        	 $elem.hide();
        	 flag = 1;
        }
        cancel = function($elem,$flag){
        	  $td = $elem.parent().prev();
        	  if($flag){
                     $td.children('span').show().text($td.children('input').val());
        	  }else if(flag){
        	  	 $td.children('span').show();
        	  	 flag = 0;
        	  }else{
        	      $elem.parents('tr').remove();
        	      return;
        	 }
             $td.children('input').remove();
             $elem.parent().children('a').show();
             $elem.parent().children('.submit,.cancel').remove();
        }
        remove = function($elem){
            confirm($elem);
            $(document).on('click','.sure',function(){
                 $.ajax({
                    url: params.url,
                    type: 'post',
                    dataType: 'text',
                    data: {data: $elem.parent().prev().children('a').text()},
                    success: function(data){
                     $elem.parents('tr').remove();
                    }
                  })
            });
            $(document).on('click','.no-remove',function(){
                $elem.parents('tr').children().show();
                $elem.parents('tr').children('.confirm').remove();
            })
        	
        }
        submit = function($elem){
        	if($elem.parent().prev().children('input').val() == ''){
        	       return;
        	}
        	$.ajax({
        		url: params.url,
        		type: 'post',
        		dataType: 'text',
        		data: {data: $elem.parent().prev().children('input').val()},
        		success:function(data){
                    cancel($elem,true);
        		}
        	})
        }
        confirm = function($elem){
            $tr = $elem.parents('tr');
            $tr.children().hide();
            $tr.append('<td class="show-offer-tpcp confirm" style="color: #f00">Are you sure to delete?</td><td class="table-handle confirm"><a class="sure btn btn-primary btn-xs">sure</a><a class="no-remove btn btn-xs">cancel</a></td>');
        }
    }
    window.editer = editer;
    $('#add-global-postback').click(function(){
        var node = '<tr id="162" data-tracking="1"><input type="hidden" value="1" class="pixelType"/><td class="show-offer-tpcp"><span></span><input type=""></td><td class="table-handle"><a href="javascript:;" class="edit" style="display: none;"><i class="glyphicon glyphicon-pencil"></i></a><a href="javascript:;" class="delete" style="display: none;"><i class="glyphicon glyphicon-trash"></i></a><a class="submit btn btn-primary btn-xs">save</a><a class="cancel btn btn-xs">cancel</a></td></tr>';
        $('.list-offer-table tbody').append(node);
    })
})(jQuery);