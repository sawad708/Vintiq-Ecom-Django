# Generated by Django 4.2.4 on 2023-10-17 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_alter_wishlist_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
    ]