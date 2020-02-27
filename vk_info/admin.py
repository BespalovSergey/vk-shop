from django.contrib import admin
from .models import UserVk, AdresesUser


@admin.register(UserVk)
class UserVkAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'available', 'phone','photo']
    list_filter = ['updated', 'available']
    list_editable = ['available']


@admin.register(AdresesUser)
class AdresesUserAdmin(admin.ModelAdmin):
    list_display = ['vk_user', 'adres', 'formadres', 'latitude', 'longitude']




