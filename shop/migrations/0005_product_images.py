# Generated by Django 2.2.6 on 2019-11-13 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20191027_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_link', models.CharField(blank=True, max_length=200, verbose_name='Ссылка на картинку Вконтакте')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.Product', verbose_name='Товар')),
            ],
        ),
    ]
