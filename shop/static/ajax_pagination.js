
$(document).ready(function(){
var page = 1;
var empty_page = false;
var block_request = false;

$(window).scroll(function(){

var margin = $(document).height()-$(window).height()-200;

if($(window).scrollTop()> margin && empty_page == false && block_request == false){

block_request = true;
page += 1;
let form = $('#filters').find('form');
let data = form.serialize();
data=data+'&page='+page;

$.get(form.attr('action'),
      data,
      function(data){

      if(data==''){empty_page = true}
      else{
      block_request = false;

      $('tbody').append(data)
      }

      })
}
});
$('#filters').on('change','[id^=id_filter_]', function(){
   page=1;
   empty_page=false;
   block_request = false;

});
});