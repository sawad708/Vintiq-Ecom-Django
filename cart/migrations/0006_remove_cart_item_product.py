# Generated by Django 4.2.4 on 2023-09-29 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cart_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart_item',
            name='product',
        ),
    ]