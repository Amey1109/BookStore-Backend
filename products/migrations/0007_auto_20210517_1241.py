# Generated by Django 3.1.1 on 2021-05-17 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20210517_1158'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_price',
            new_name='order_discount',
        ),
    ]
