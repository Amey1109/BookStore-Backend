# Generated by Django 3.1.1 on 2021-05-17 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20210517_1241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_discount',
            new_name='order_price',
        ),
    ]
