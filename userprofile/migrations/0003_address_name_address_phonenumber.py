# Generated by Django 4.2.2 on 2023-09-13 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='phonenumber',
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
    ]
