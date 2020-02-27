from django.db import models
from django.conf import settings
from pytils.translit import slugify
from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from vk_info.models import UserVk
from decimal import Decimal

class AccountManager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Мэнеджер'
        verbose_name_plural = 'Мэнеджеры'

    def __str__(self):
        return '{}'.format(self.user.first_name)


class Shop(models.Model):
    manager = models.OneToOneField(AccountManager, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='Название магазина')
    slug = models.SlugField(max_length=200, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = '{}{}'.format(slugify(self.name),self.pk)
        super(Shop, self).save(*args, **kwargs)


class Bot(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE , verbose_name='Магазин')
    vk_group_id = models.CharField(max_length=50, unique=True, blank=True, null=True,
                                   verbose_name='Id группы Вконтакте')
    is_active = models.BooleanField(default=False)
    process_name = models.CharField(max_length=50, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'

    def __str__(self):
        return 'Бот магазина {}'.format(self.shop)


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='Слаг')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,
                             related_name='categories')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        index_together = (('shop', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_detail', args=[self.id, self.slug])

    def get_delete_url(self):
        return reverse('shop:delete_category', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        self.slug = '{}'.format(slugify(self.name))
        super(Category, self).save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название товара')
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='Слаг')
    description = models.TextField(max_length=1000,blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    availabel = models.BooleanField(default=True , verbose_name='Доступнось')
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE, verbose_name='Категория')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id','slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = '{}'.format(slugify(self.name))
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id])

    def get_delete_url(self):
        return reverse('shop:delete_product', args=[self.id])


class CartItem(models.Model):
    product = models.ForeignKey(Product, related_name='cart_items',
                                on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2,default=0.00)

    class Meta:
        verbose_name = 'Продукт корзины'
        verbose_name_plural = 'Продукты корзины'
    def __str__(self):
        return 'Часть корзины для продукта {}'.format(self.product.name)

    def add_product(self, product):
        self.qty += 1
        self.item_total = product.price * self.qty
        self.save()


    def remove_product(self,product):
        self.qty -=1
        if self.qty > 0: self.item_total = product.price * self.qty
        self.save()


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    shop = models.ForeignKey(Shop, blank=True, null=True, on_delete=models.CASCADE, related_name='carts')
    user = models.ForeignKey(UserVk, blank=True, null=True, on_delete=models.CASCADE, related_name='carts')
    vk_id = models.CharField(max_length=21,null=True, verbose_name='Вк айди')
    cart_total = models.DecimalField(max_digits=9, decimal_places=2,
                                     default=0.00)
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, product_id):
        cart = self
        product = get_object_or_404(Product, pk=product_id)
        for item in cart.items.all():

            if product == item.product:

                item.add_product(product)
                self.update_cart_total()
                cart.save()
                return
        cart.items.add(CartItem.objects.create(product=product, item_total=product.price))
        self.update_cart_total()
        cart.save()


    def remove_frorm_cart(self,product_id):

        cart = self
        product = get_object_or_404(Product, pk=product_id)
        for item in cart.items.all():
            if product == item.product:

                if item.qty > 1:
                    item.remove_product(product)
                    self.update_cart_total()
                    cart.save()
                    return
                else:
                    cart.items.remove(item)
                    self.update_cart_total()
                    cart.save()
                    item.delete()
                    return
        raise APIException('Product not in cart')


    def update_cart_total(self):
        self.cart_total= sum([item.item_total for item in self.items.all()])


class Product_images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images',verbose_name='Товар')
    image_link = models.CharField(max_length=200, verbose_name='Ссылка на картинку Вконтакте')
    file_url = models.CharField(max_length=200, blank=True, null=True, verbose_name='Путь к файлу')

    class Meta:
        verbose_name = 'Изабражение товара'
        verbose_name_plural = 'Изображения товаров'
    def save(self, *args, **kwargs):
        if len(self.product.images.all()) <= 4:
            super(Product_images, self).save(*args, **kwargs)


ORDER_STATUS_CHOICES = (
    ('Предзаказ', 'Предзаказ'),
    ('Принят', 'Принят'),
    ('Отправлен', 'Отправлен'),
    ('Оплачен', 'Оплачен')
)

class Order(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders', verbose_name='Магазин')
    user = models.ForeignKey(UserVk, on_delete=models.CASCADE, related_name='orders', verbose_name='Покупатель')
    order_status = models.CharField(max_length=25, choices=ORDER_STATUS_CHOICES, verbose_name='Статус заказа')
    delivery = models.CharField(max_length=25, blank=True, null=True, choices=(('Доставка', 'Доставка'), ('Самовывоз', 'Самовывоз')), verbose_name='Способ доставки')
    adres = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес доставки')
    phone = models.CharField(max_length=25, blank=True, null=True, verbose_name='Телефон')
    total_summ = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Общая сумма')
    products = models.CharField(max_length=255, blank=True, null=True, verbose_name='Товары')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-id']

    def delete_product(self, product_id):
        product_list = self.products.split('%&')
        for i, product in enumerate(product_list):
            items = product.split('@#')
            if int(items[0]) == product_id:
                price = Decimal(float(items[3]) / int(items[2]))
                self.total_summ = self.total_summ - price
                items[2] = int(items[2]) - 1
                if items[2]:
                    items[2] = str(items[2])
                    items[3] = str(Decimal(items[3])-price)
                    product_list[i] = '@#'.join(items)
                else:
                    product_list.pop(i)
        self.products = '%&'.join(product_list)
        self.save()
