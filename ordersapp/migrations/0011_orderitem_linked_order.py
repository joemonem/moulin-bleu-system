# Generated by Django 5.0 on 2024-01-02 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ordersapp", "0010_remove_orderitem_linked_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="linked_order",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="ordersapp.order",
            ),
        ),
    ]