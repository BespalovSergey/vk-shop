from rest_framework import serializers
from ..models import Product, Shop, Category, Cart, CartItem, Product_images, Order
from vk_info.models import UserVk, AdresesUser


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'shop']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_images
        fields = ['image_link', 'file_url']


class ProductSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(read_only = True, many = True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'slug', 'price', 'category', 'images', 'shop']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['product', 'qty', 'item_total']


class CartSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)
    items = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = ['id', 'vk_id', 'cart_total', 'items', 'shop']


class AdresesUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdresesUser
        fields = ['id', 'adres', 'formadres', 'latitude', 'longitude']


class UserVkSerializer(serializers.ModelSerializer):
    adreses = AdresesUserSerializer(read_only=True, many=True)
    class Meta:
        model = UserVk
        fields = ['id', 'first_name', 'last_name', 'photo','phone', 'adreses']


class OrderSerializer(serializers.ModelSerializer):
    user = UserVkSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'shop', 'user', 'order_status', 'delivery', 'adres', 'phone', 'total_summ', 'products']
