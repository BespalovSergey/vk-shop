from django.db import models


class UserVk(models.Model):
    user_ids = models.CharField(max_length=100, verbose_name='ID пользователя')
    domain = models.CharField(max_length=100, null=True, verbose_name='Ссылка на страницу пользователя')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Фамилие')
    photo = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ссылка на фото')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Пользователь Вк'
        verbose_name_plural = 'Пользователи Вк'

    def update_user_vk(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value
        self.save()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class AdresesUser(models.Model):
    vk_user = models.ForeignKey(UserVk, on_delete=models.CASCADE , related_name='adreses')
    adres = models.CharField(max_length=255, verbose_name='Адресс доставки пользователя')
    formadres = models.CharField(max_length=255, blank=True, null=True, verbose_name='Форматированный адрес')
    latitude = models.CharField(max_length=25, blank=True, null=True, verbose_name='Широта')
    longitude = models.CharField(max_length=25, blank=True, null=True, verbose_name='Долгота')

    class Meta:
        verbose_name = 'Адрес пользователя Вк'
        verbose_name_plural = 'Адреса пользователей Вк'
    def save(self, *args, **kwargs):
        adreses = self.vk_user.adreses.all()

        super(AdresesUser, self).save(*args, **kwargs)
        if len(adreses) > 5:
            adreses[0].delete()



