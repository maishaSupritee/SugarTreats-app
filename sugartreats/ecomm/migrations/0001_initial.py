# Generated by Django 4.2 on 2023-06-17 18:30

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
                ("name", models.CharField(max_length=200, null=True)),
                ("email", models.CharField(max_length=200, null=True)),
                ("phone", models.CharField(max_length=200, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=200, null=True)),
                ("product_num", models.CharField(max_length=100, unique=True)),
                ("description", models.CharField(max_length=200, null=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Core", "Core"),
                            ("Vegan", "Vegan"),
                            ("Alcoholic", "Alcoholic"),
                            ("Coffee", "Coffee"),
                            ("Tea", "Tea"),
                        ],
                        max_length=200,
                        null=True,
                    ),
                ),
                ("price", models.FloatField(null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                ("tags", models.ManyToManyField(to="ecomm.tag")),
            ],
        ),
    ]
