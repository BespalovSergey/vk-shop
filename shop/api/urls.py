from django.urls import path
from . import views

app_name = 'apishop'

urlpatterns=[
    # path('products', views.ProductListView.as_view(), name='api_product_list'),
    path('product_detail', views.ProductDetailView.as_view(), name='api_product_detail'),
    path('get_cart', views.CartView.as_view(), name='api_get_cart'),
    path('add_to_cart', views.AddToCartView.as_view(), name='api_add_to_cart'),
    path('remove_from_cart', views.RemoveFromCartView.as_view(), name='api_remove_from_cart'),
    path('products', views.ProductListView.as_view(), name='api_product_list'),
    path('categorys', views.CategoryListView.as_view(), name='api_category_list'),
    path('user_adreses', views.UserAdresesView.as_view(), name='api_user_adreses'),
    path('add_user_adres', views.AddUserAdresView.as_view(), name='api_add_user_adres'),
    path('remove_user_adres', views.RemoveUserAdresView.as_view(), name='api_remove_user_adres'),
    path('user_adres', views.UserAdresView.as_view(), name='api_user_adres'),
    path('add_order_adres', views.AddOrderAdres.as_view(), name='api_add_order_adres'),
    path('add_order_phone', views.AddOrderPhone.as_view(), name='api_add_order_phone')

]