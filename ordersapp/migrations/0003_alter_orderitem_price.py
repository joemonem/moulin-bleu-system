# Generated by Django 5.0 on 2023-12-29 10:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ordersapp", "0002_alter_orderitem_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="price",
            field=models.DecimalField(
                auto_created=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
