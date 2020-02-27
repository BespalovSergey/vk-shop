$(document).ready(function(){


$('#table-content').on('click', 'a.p-item', function(){
item_id = $(this).attr('pid')
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

$('#table-content').on('click','[id^=dop-]', function(){
let product_table = $(this).parent().parent().parent().parent()
let prod_id = $(this).attr('id').slice(4)
let order_id = product_table.attr('order-id')
let url='del_order_product'
let data = {}
data['product'] = prod_id
data['order'] = order_id
let csrf_token = $('#table-content').find('input[name=csrfmiddlewaretoken]')
data['csrfmiddlewaretoken'] = csrf_token.val()
$.post(
url,
data,
function(data){
product_table.html(data.products)
$('#total-'+order_id).text(data.total_summ)
}
);



});


});