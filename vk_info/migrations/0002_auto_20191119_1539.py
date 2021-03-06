# Generated by Django 2.2.6 on 2019-11-19 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vk_info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservk',
            name='domain',
            field=models.CharField(max_length=100, null=True, verbose_name='Ссылка на страницу пользователя'),
        ),
        migrations.AlterField(
            model_name='adresesuser',
            name='vk_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adreses', to='vk_info.UserVk'),
        ),
        migrations.AlterField(
            model_name='uservk',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилие'),
        ),
        migrations.AlterField(
            model_name='uservk',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='uservk',
            name='photo',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ссылка на фото'),
        ),
    ]
