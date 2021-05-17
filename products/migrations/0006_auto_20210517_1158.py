# Generated by Django 3.1.1 on 2021-05-17 06:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_price',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_of_delivery',
            field=models.DateField(default=datetime.date(2021, 5, 24)),
        ),
    ]
