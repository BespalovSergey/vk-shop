from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from  shop.models import AccountManager, Shop, Bot


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.username = user_form.cleaned_data['email']
            new_user.save()
            manager =  AccountManager.objects.create(user=new_user)
            shop = Shop.objects.create(manager= manager, name='Ваш магазин {}'.format(manager.user.first_name))
            Bot.objects.create(shop= shop)
            return render(request, 'registration/register_done.html',
                          {'new_user':new_user.first_name, 'register_done': True})
    else:
        user_form = UserRegistrationForm()
    return  render(request, 'registration/register.html', {'user_form': user_form})
