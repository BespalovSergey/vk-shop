from django.shortcuts import render, redirect, get_object_or_404
from .forms import ShopForm, BotForm, CategoryForm, ProductForm, ProductFilterForm, ProductImagesForm
from .models import Category, Product, Cart, CartItem, Product_images, Order
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from common.decorators import ajax_required
from django.http import HttpResponse
from django.template.loader import render_to_string
import json
import requests
from bs4 import BeautifulSoup
from . import utils
from decimal import Decimal


def dashboard(request):
    return render(request, 't_base.html')


def shop_detail(request):
    if request.method == 'POST':
        shop = request.user.accountmanager.shop
        shop_form = ShopForm(request.POST, instance=shop)
        bot_form = BotForm(request.POST, instance=shop.bot)

        if shop_form.is_valid() and bot_form.is_valid():
            shop_form.save()
            bot_form.save()
            return redirect('shop:dashboard')
    else:
        user = request.user
        shop = user.accountmanager.shop
        bot = shop.bot
        shop_form = ShopForm(instance=shop)
        bot_form = BotForm(instance=bot)
    return render(request, 'dashboard/shop_detail.html', {'shop_form': shop_form,
                                                          'bot_form': bot_form})


def category_list(request):
    if request.method == 'GET':
        categorys = Category.objects.filter(shop=request.user.accountmanager.shop)
        return render(request, 'dashboard/category/category_list.html',
                      {'categorys': categorys, 'update_link': 'category_detail/', 'create_link': 'create_category'})


def category_detail(request, id=None, slug=None):

    category = None
    if request.method == 'POST':
        if id and slug:
            category = get_object_or_404(Category, id=id, slug=slug, shop=request.user.accountmanager.shop)
            category_form = CategoryForm(request.POST, instance=category)
            if category_form.is_valid() and request.is_ajax():
                category_form.save()
                data = {'result':'update_row',
                        'content':render_to_string('dashboard/category/category_row.html', {'category': category})}
                return HttpResponse(json.dumps(data), content_type='application/json')

        else:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category = category_form.save(commit=False)
                category.shop = request.user.accountmanager.shop
                category.save()
                data = {'result': 'add_row',
                        'content': render_to_string('dashboard/category/category_row.html', {'category': category})}
                return HttpResponse(json.dumps(data), content_type='application/json')


    else:
        if id and slug:
            category = get_object_or_404(Category, id=id, slug=slug, shop=request.user.accountmanager.shop)
            category_form = CategoryForm(instance=category)

        else:
            category_form = CategoryForm()

    data = {'result': 'form', 'content': render_to_string('dashboard/category/category_detail.html', {'category_form': category_form, 'category': category }, request)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def delete_category(request, id, slug):
    if request.method == 'GET':
        category = get_object_or_404(Category, id=id, slug=slug, shop=request.user.accountmanager.shop)
        category.delete()
        return HttpResponse(json.dumps({'result':'OK'}), content_type='application/json')


def product_list(request):
    if request.method == 'GET':
        products = Product.objects.filter(shop=request.user.accountmanager.shop)
        filter_form = ProductFilterForm(request, data=request.GET)

        if filter_form.is_valid() and request.is_ajax():
            for k, v in filter_form.cleaned_data.items():
                if v:
                    if k == 'filter_category': products = products.filter(category=v)
                    if k == 'filter_availabel': products = products.filter(availabel=v)

        pag = 10

        paginator = Paginator(products, pag)
        page = request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            products = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request, 'dashboard/goods/product_list_ajax.html', {'products': products})

        return render(request,'dashboard/goods/product_list.html',{'products':products,
                       'update_link': 'product_detail/', 'create_link': 'create_product','filters':filter_form})


def product_detail(request, id=None):
    product = None
    categorys = Category.objects.filter(shop=request.user.accountmanager.shop)
    if request.method == 'POST':
        if id :
            product = get_object_or_404(Product, id=id, shop=request.user.accountmanager.shop)
            product_form = ProductForm(chois_cats=categorys, data=request.POST, instance=product )
            if product_form.is_valid() and request.is_ajax():
                product.save()

                data = {'result': 'update_row',
                        'content': render_to_string('dashboard/goods/product_row.html', {'product': product})}
                return HttpResponse(json.dumps(data), content_type='application/json')

        else:
            product_form = ProductForm(data=request.POST, chois_cats=categorys)
            if product_form.is_valid() and request.is_ajax():
                product = product_form.save(commit=False)
                product.shop = request.user.accountmanager.shop
                product.save()
                data = {'result': 'add_row',
                        'content': render_to_string('dashboard/goods/product_row.html', {'product': product})}
                return HttpResponse(json.dumps(data), content_type='application/json')


    else:
        if id :
            product = get_object_or_404(Product, id=id, shop=request.user.accountmanager.shop)
            images_forms = []
            for image in product.images.all():
                images_forms.append((ProductImagesForm(instance=image), image))
            if len(images_forms)<4:
                images_forms.append((ProductImagesForm(), None))
            product_form = ProductForm(instance=product, chois_cats=categorys)

        else:
            images_forms = [(ProductImagesForm, None)]
            product_form = ProductForm(chois_cats=categorys)

    data = {'result': 'form', 'content': render_to_string('dashboard/goods/product_detail.html',
                                                          {'product_form': product_form, 'product': product, 'images': images_forms},
                                                          request)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def delete_product(request, id):
    if request.method == 'GET':
        product = get_object_or_404(Product, id=id)
        product.delete()
        return HttpResponse(json.dumps({'result': 'OK'}), content_type='appliction/json')


def cart_list(request):
    if request.method == 'GET':
        carts = Cart.objects.filter(shop=request.user.accountmanager.shop)
        pag = 10

        paginator = Paginator(carts, pag)
        page = request.GET.get('page')

        try:
            carts = paginator.page(page)
        except PageNotAnInteger:
            carts = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            carts = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request, 'dashboard/carts/cart_list_ajax.html', {'carts': carts})

        return render(request, 'dashboard/carts/cart_list.html', {'carts': carts})


def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.filter(shop=request.user.accountmanager.shop)
        pag = 10
        paginator = Paginator(orders, pag)
        page = request.GET.get('page')
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            orders = paginator.page(paginator.num_pages)
            if request.is_ajax():
                return render(request, 'dashboard/orders/order_list_ajax.html', {'orders':orders})
        return render(request, 'dashboard/orders/order_list.html', {'orders': orders})



@ajax_required
def get_link_photo_file(request):
    data = {'result': 'bad'}
    vk_url = request.GET.get('vk_url')
    if 'https://vk.com/' in vk_url:
        vk_url = vk_url[vk_url.rfind('z=')+2:]
        vk_url = 'https://vk.com/{}?rev=1'.format(vk_url[:vk_url.find('%')])
        response = requests.get(vk_url)

        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.text,'html.parser')
            div = soup.find(class_='pv_photo_wrap')
            if div:
                src = div.find('img')['src']
                if 'https://' in src:
                    data = {'result':'ok',
                            'url':src}

    return HttpResponse(json.dumps(data), content_type='application/json')

@ajax_required
def add_product_image(request, ppk, ipk=None):
    data = {'result': 'bad'}
    if request.method == 'POST':
        if ipk:
            image = get_object_or_404(Product_images,pk=ipk)
            image_form = ProductImagesForm(data=request.POST, instance=image)
            if image_form.is_valid():
                image.file_url = utils.get_file_url(image.image_link)
                image.save()
                data = {'result': 'update',
                        'content': render_to_string('dashboard/goods/image_form.html',
                                                    {'image': image, 'form': image_form,
                                                     'product': image.product},
                                                    request)}
        else:
            product = get_object_or_404(Product, pk=ppk)
            image_form = ProductImagesForm(data=request.POST)
            if image_form.is_valid():
                image = image_form.save(commit=False)
                image.file_url = utils.get_file_url(image.image_link)
                image.product = product
                image.save()
                data = {'result': 'add',
                        'content': render_to_string('dashboard/goods/image_form.html',
                                                    {'image': image, 'form': image_form,
                                                     'product': image.product,},
                                                    request),
                        'empty_form': render_to_string('dashboard/goods/image_form.html', {'form': ProductImagesForm(),
                                                                                           'image': None,
                                                                                           'product': product}, request)
                        }
    return HttpResponse(json.dumps(data), content_type='application/json')

@ajax_required
def remove_product_image(request, pk):
    data = {'result': 'bad'}
    if request.method == 'GET':
        image = get_object_or_404(Product_images, pk=pk)
        product = image.product
        if image.product.shop == request.user.accountmanager.shop:
            image.delete()
            data = {'result': 'ok',
                    'empty_form': render_to_string('dashboard/goods/image_form.html', {'form': ProductImagesForm(),
                                                                                       'image': None,
                                                                                       'product': product}, request)
                   }
    return HttpResponse(json.dumps(data), content_type='application/json')


@ajax_required
def del_order_product(request):
    if request.method == 'POST':
        order_id = int(request.POST.get('order'))
        product_id = int(request.POST.get('product'))
        order = get_object_or_404(Order, pk=order_id)
        order.delete_product(product_id)
        products = render_to_string('dashboard/orders/order_products.html', {'order': order}, request)

    return HttpResponse(json.dumps({'products': products, 'total_summ':str( order.total_summ)}), content_type='application/json')
