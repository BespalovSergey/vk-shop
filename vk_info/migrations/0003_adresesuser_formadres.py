# Generated by Django 2.2.6 on 2019-11-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vk_info', '0002_auto_20191119_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='adresesuser',
            name='formadres',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Форматированный адрес'),
        ),
    ]
