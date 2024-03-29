# Generated by Django 5.0 on 2024-01-02 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ordersapp", "0008_order_delivery"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="linked_order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="ordersapp.order",
            ),
        ),
    ]
