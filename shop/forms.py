from django.contrib.auth.models import User
from django import forms
from .models import Shop, Bot, Category, Product, Product_images, Order


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name',)


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        exclude = ('process_name', 'is_active', 'shop')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('shop','slug')


class ProductForm(forms.ModelForm):

    class Meta:
        model= Product
        exclude = ('slug', 'shop', 'created', 'updated')

    def __init__(self,chois_cats, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=chois_cats, label='Категория')


class ProductFilterForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        request = request
        super(ProductFilterForm,self).__init__(*args, **kwargs)

        self.fields['filter_category'] = forms.ModelChoiceField(queryset=Category.objects.filter(shop= request.user.accountmanager.shop),
                                            label='Категория', required=False)
        self.fields['filter_availabel'] = forms.BooleanField(required=False, label='Доступные')

class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = Product_images
        fields = ('image_link',)


class OrderFrom(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('user', 'products', 'adres', 'phone', 'order_status')
