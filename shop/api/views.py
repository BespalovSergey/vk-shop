from ..models import Product, Category, Cart, CartItem, Product_images , Order
from .serializers import ProductSerializer, CategorySerializer, CartSerializer,\
                        CartItemSerializer, ProductImageSerializer, UserVkSerializer,\
                        AdresesUserSerializer, OrderSerializer
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import paginations_items
from vk_info.models import UserVk, AdresesUser
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from geopy.geocoders import Nominatim


class CartView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_id = request.GET.get('cart_id')
        cart, _ = Cart.objects.get_or_create(vk_id=cart_id , shop=request.user.accountmanager.shop)
        item_count = 5
        page = request.GET.get('page')
        cart_items = cart.items.all().order_by('id')
        cart_items, page, num_page = paginations_items(cart_items, page, item_count)
        cart = CartSerializer(cart)
        cart_items = CartItemSerializer(cart_items, many=True)
        return Response({'cart': cart.data, 'cart_items': cart_items.data, 'page': page, 'num_page': num_page})


class AddToCartView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        id = request.POST.get('pk')
        user_id = request.POST.get('user_id')
        cart, _ = Cart.objects.get_or_create(vk_id=user_id, shop=request.user.accountmanager.shop)
        cart.add_to_cart(product_id=id)

        return Response({'cart':'Added'})


class RemoveFromCartView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        pk = request.POST.get('ppk')
        vk_id = request.POST.get('vk_id')
        cart = get_object_or_404(Cart, vk_id=vk_id, shop=request.user.accountmanager.shop)
        cart.remove_frorm_cart(product_id=pk)
        return Response({'result': 'OK'})


class CategoryListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categorys = Category.objects.annotate(one=Count('products')).filter(shop=request.user.accountmanager.shop, one__gt=0)
        item_count = 10
        page = request.GET.get('page')
        categorys, page, num_page = paginations_items(categorys, page, item_count)
        categorys = CategorySerializer(categorys, many=True)
        return Response({'categorys': categorys.data, 'num_page': num_page,
                         'item_count': item_count, 'page': page})


class ProductListView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category_id = int(request.GET.get('pk'))
        products = Product.objects.filter(category=category_id)
        item_count = 10
        page = request.GET.get('page')
        products, page, num_page = paginations_items(products, page, item_count)
        products = ProductSerializer(products, many=True)
        return Response({'products': products.data, 'num_page':num_page,
                         'item_count': item_count, 'page':page})


class ProductDetailView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        product_id = request.GET.get('pk')
        vk_id = request.GET.get('v_id')
        prod = get_object_or_404(Product, pk=product_id)
        product = ProductSerializer(prod)
        cart, _ = Cart.objects.get_or_create(shop=request.user.accountmanager.shop, vk_id=vk_id)
        cart_item = None
        for item in cart.items.all():
            if item.product == prod:
                cart_item = CartItemSerializer(item).data
        return Response({'product': product.data, 'cart_item': cart_item})


class UserAdresesView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #c_id = request.POST.get('c_id')
        vk_id = request.POST.get('vk_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        photo = request.POST.get('phot')
        domain = request.POST.get('domain')
        try:
            vk_user = UserVk.objects.get(user_ids=vk_id)
            vk_user.update_user_vk(first_name=first_name, last_name=last_name, photo=photo, domain=domain)
        except ObjectDoesNotExist:
            vk_user = UserVk.objects.create(user_ids=vk_id, first_name=first_name, last_name=last_name, photo=photo,
                                            domain=domain)
        cart, _ = Cart.objects.get_or_create(shop=request.user.accountmanager.shop, vk_id=vk_id)
        cart.user = vk_user
        cart.save()
        vk_user = UserVkSerializer(vk_user)
        return Response({'vk_user': vk_user.data})


class AddUserAdresView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    def post(self, request):
        vk_id = request.POST.get('vk_id')
        adres = request.POST.get('adres')
        lat, lon, fadres = None, None, None
        try:
            coder = Nominatim()
            result_coder = coder.geocode(adres, exactly_one=True)
            if result_coder.address:
                lat = result_coder.latitude
                lon = result_coder.longitude
                al = result_coder.address.split(',')
                fadres ='{}, {}, {}, {}, {}'.format(al[4], al[3], al[2], al[1], al[0])
        except:
            pass
        vk_user = get_object_or_404(UserVk)
        user_adres = AdresesUser.objects.create(vk_user=vk_user,adres=adres ,formadres=fadres,
                                                latitude=lat, longitude =lon)
        user_adres = AdresesUserSerializer(user_adres)
        return Response({'adres': user_adres.data['id']})


class RemoveUserAdresView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    def post(self, request):
        pk = request.POST.get('pk')
        adres = get_object_or_404(AdresesUser, pk=pk)
        adres.delete()
        return Response({'result': 'ok'})

class UserAdresView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self,request):
        pk = request.GET.get('pk')
        adres = get_object_or_404(AdresesUser, pk=pk)
        adres = AdresesUserSerializer(adres)
        return Response({'adres':adres.data})

class AddOrderAdres(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        adres_id = request.POST.get('pk')
        vk_id = request.POST.get('vk_id')
        adres = get_object_or_404(AdresesUser, pk=adres_id)
        user_vk = get_object_or_404(UserVk, user_ids=vk_id)
        cart = get_object_or_404(Cart, vk_id=vk_id, shop=request.user.accountmanager.shop)
        try:
            order = Order.objects.get(user=user_vk, shop=request.user.accountmanager.shop, order_status='Предзаказ')
        except ObjectDoesNotExist:
            order = Order.objects.create(user=user_vk, shop=request.user.accountmanager.shop, order_status='Предзаказ')
        except MultipleObjectsReturned:
            pass
        order_adres = ''
        for i, field in enumerate(['adres', 'formadres', 'latitude', 'longitude']):
            d = ''
            if adres.__dict__[field]:
                if i != 0: d = '%&'
                order_adres = '{}{}{}'.format(order_adres, d, adres.__dict__[field])
        order.adres = order_adres
        cart_items = cart.items.all()
        product_ids = ''
        for i, item in enumerate(cart_items):
            d=''
            if i != 0: d = '%&'
            product_ids = '{}{}{}@#{}@#{}@#{}'.format(product_ids, d, item.product.id, item.product.name, item.qty, item.item_total)
        order.products = product_ids
        order.total_summ = cart.cart_total
        order.save()
        order = OrderSerializer(order)
        return Response({'order':order.data})


class AddOrderPhone(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        vk_id = request.POST.get('vk_id')
        phone = request.POST.get('phone')
        user_vk = get_object_or_404(UserVk, user_ids=vk_id)
        order = None
        try:
            order = Order.objects.get(user=user_vk, shop=request.user.accountmanager.shop, order_status='Предзаказ')
        except ObjectDoesNotExist:
            order = Order.objects.create(user=user_vk, shop=request.user.accountmanager.shop, order_status='Предзаказ')
        except MultipleObjectsReturned:
            pass
        if order:
            user_vk.phone = phone
            user_vk.save()
            order.phone = phone
            order.save()
            order = OrderSerializer(order).data
        return Response({'order': order})









