def menu(request):
    user = request.user
    menu = []
    if user.is_authenticated:
        if hasattr(user,'accountmanager'):
            menu = [
                {'type': 'item', 'icon': 'fa-tablet', 'link': 'shop:shop_detail', 'text': 'Магазин'},
                {'type': 'item', 'icon': 'fa-reorder', 'link': 'shop:order_list', 'text': 'Заказы'},
                {'type': 'item', 'icon': 'fa-inbox', 'link': 'shop:category_list', 'text': 'Категории'},
                {'type': 'item', 'icon': 'fa-support ', 'link': 'shop:product_list', 'text': 'Товары'},
                {'type': 'item', 'icon': 'fa-shopping-cart', 'link':'shop:cart_list', 'text': 'Брошенные корзины'},

            ]


    return {'menu':menu}