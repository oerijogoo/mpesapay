# Generated by Django 4.2.16 on 2024-11-13 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(db_index=True, max_length=255)),
                ("slug", models.SlugField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "categories",
            },
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
                ("title", models.CharField(max_length=255)),
                ("brand", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("slug", models.SlugField(max_length=255)),
                ("price", models.DecimalField(decimal_places=2, max_digits=4)),
                ("image", models.ImageField(upload_to="images/")),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="store.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "products",
            },
        ),
    ]
