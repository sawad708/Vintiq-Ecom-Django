# Generated by Django 4.2.4 on 2023-09-24 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_rename_copon_code_coupon_coupon_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.DeleteModel(
            name='productImage',
        ),
    ]