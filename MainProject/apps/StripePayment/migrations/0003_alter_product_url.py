# Generated by Django 4.2.5 on 2023-12-28 21:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("StripePayment", "0002_product_file_product_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="url",
            field=models.URLField(),
        ),
    ]