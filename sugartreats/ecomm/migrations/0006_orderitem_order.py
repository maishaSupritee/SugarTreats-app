# Generated by Django 4.2 on 2023-08-31 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ecomm", "0005_alter_customer_email_alter_order_note_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="ecomm.order"
            ),
        ),
    ]
