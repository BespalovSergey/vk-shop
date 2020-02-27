$(document).ready(function(){
var item_id = -1



$('#table-content').on('click','a.item', function(){
item_id = $(this).attr('id')
let url = $('table').attr('target-link')+item_id

$.get(

url,

function(data){

$('#detail-content').html(data)
   if(data['result'] == 'form'){
   $('#detail-content').html(data['content'])
   data_settings_submit(item_id)
   image_submit()
   }
}
);
});





$('#create-item').on('click', function(){
  $.get(
    $(this).attr('target-link'),
    function(data){
    if(data['result'] == 'form'){
    $('#detail-content').html(data['content']);
    data_settings_submit(item_id);
    image_submit();
    }
    }
  );
});



$('#modal-default').on('click','#delete-item', function(){

$.get(
  $(this).attr('target-link'),
  function(data){

  if (data['result'] == 'OK'){
     $('#'+item_id).parent().parent().remove()
  }

  }
)
})



$('#filters').on('change','[id^=id_filter_]', function(){
let form = $('#filters').find('form')

$.get(
   form.attr('action'),
   form.serialize(),
   function(data){
   $('tbody').html(data)

   }
);

});




});



function data_settings_submit(item_id){
  $('#data_settings').submit( function(){

let form = $(this)

$.post(
    form.attr('action'),
    form.serialize(),
    function(data){

     if(data['result'] == 'form'){
     $('#detail-content').html(data['content'])

     }else if(data['result'] == 'update_row'){
      $('#'+item_id).parent().parent().replaceWith(data['content']);
      $('#close-modal-default').click();
      console.log(data)
        }else{
         $('tbody').append(data['content']);
         $('#close-modal-default').click();
        }
    }
);
return false;
});
}

function image_submit(){
$('#image_settings').on('submit','form',function(){
let form = $(this)
$.post(
form.attr('action'),
form.serialize(),
function(data){
let result = data['result'];
if (result == 'update'){
   let div_id = '#'+form.attr('action')
   form.parent().replaceWith(data['content'])
  }else if(data['result'] == 'add'){
   form.parent().remove()
   $('#image_settings').append(data['content'])
   if ($('.image-form').length < 4){
     $('#image_settings').append(data['empty_form'])
   }
  }
}
)
return false;
});

$('#image_settings').on('click','button',function(){
let btn = $(this)
let url = btn.attr('link')
let id  = url.slice( url.lastIndexOf('/')+1)
let divs = $('.image-form')
$.get(
url,
{},
function(data){
if (data['result'] == 'ok'){
   $('#image-'+id).remove()
   if (divs.length >= 4 ){
       $('#image_settings').append(data['empty_form'])
     }
  }
}
)

});

}
