from django.contrib import admin
from .models import AccountManager, Category, Product, Bot, Shop, CartItem, Cart, Product_images, Order

@admin.register(AccountManager)
class AccountManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'user']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['shop','name','slug']
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price','category', 'availabel', 'created', 'updated']
    list_filter = ['availabel', 'created', 'updated']
    list_editable = ['price', 'availabel']
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product_images)
class Product_imagesAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_link']
    list_filter = ['product']


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'manager']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ['shop', 'is_active', 'process_name']
    list_filter = ['shop']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product','qty', 'item_total']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['shop', 'vk_id', 'cart_total']
    list_filter = ['shop', 'vk_id']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['shop', 'user', 'delivery', 'adres', 'phone', 'products', 'total_summ', 'order_status']
    list_filter =  ['shop', 'user', 'delivery', 'order_status']

