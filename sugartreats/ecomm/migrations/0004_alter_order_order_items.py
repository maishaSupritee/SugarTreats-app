# Generated by Django 4.2 on 2023-08-27 06:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ecomm", "0003_product_rewards"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_items",
            field=models.ManyToManyField(related_name="orders", to="ecomm.orderitem"),
        ),
    ]