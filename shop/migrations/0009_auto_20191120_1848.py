# Generated by Django 2.2.6 on 2019-11-20 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery',
            field=models.CharField(blank=True, choices=[('Доставка', 'Доставка'), ('Самовывоз', 'Самовывоз')], max_length=25, null=True, verbose_name='Способ доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Товары'),
        ),
    ]
