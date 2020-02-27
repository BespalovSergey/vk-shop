from django import template
from .. import models

register = template.Library()


@register.filter(name='short_adres')
def short_adres_format(text, marker):
    index = text.find(marker)
    if index != -1:
        text = text[0:index]
    return text

@register.filter(name='isdigits')
def digits_id(text):
    return text.isdigit()


@register.inclusion_tag(filename='shop_tag_templates/order_status.html' , name='order_status' )
def select_status(order):
    context = {'status': order.order_status,
               'items': []}
    for i , status in enumerate(models.ORDER_STATUS_CHOICES):
        item = {'value': i, 'name': status[0], 'selected': False}
        if status[0] == order.order_status:
            item['selected'] = True
        context['items'].append(item)
    return {'context': context}

@register.inclusion_tag(filename='shop_tag_templates/order_products.html', name='order_products')
def order_product_view(order):
    prod_text = order.products.split('%&')
    products = []
    for item in prod_text:
        item_list = item.split('@#')
        if len(item_list) > 1 :
            product = {'id':item_list[0], 'name': item_list[1], 'count': item_list[2], 'total': item_list[3]}
            products.append(product)
    return {'products':products, 'order_id': order.id}


