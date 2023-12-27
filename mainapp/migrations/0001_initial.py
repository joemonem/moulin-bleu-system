# Generated by Django 5.0 on 2023-12-26 14:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("phone_number", models.CharField(max_length=255)),
                ("location", models.CharField(max_length=255)),
                ("date_added", models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
