from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('',views.dashboard, name= 'dashboard'),
    path('shop_detail', views.shop_detail, name= 'shop_detail'),

    path('category_list', views.category_list, name='category_list'),
    path('create_category', views.category_detail, name='create_category'),
    path('category_detail/<int:id>/<slug:slug>', views.category_detail, name='category_detail'),
    path('delete_category/<int:id>/<slug:slug>', views.delete_category, name='delete_category'),

    path('product_list', views.product_list, name='product_list'),
    path('create_product', views.product_detail, name='create_product'),
    path('product_detail/<int:id>', views.product_detail, name='product_detail'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),

    path('cart_list', views.cart_list, name='cart_list'),
    path('url_photo_file', views.get_link_photo_file, name='url_photo_file'),

    path('add_product_image/<int:ppk>', views.add_product_image, name='add_product_image'),
    path('add_product_image/<int:ppk>/<int:ipk>', views.add_product_image, name='update_product_image'),
    path('remove_product_image/<int:pk>', views.remove_product_image, name='remove_product_image'),

    path('orders', views.order_list, name='order_list'),
    path('del_order_product', views.del_order_product, name='delete_order_product'),


]