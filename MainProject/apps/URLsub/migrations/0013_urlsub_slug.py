# Generated by Django 4.2.5 on 2023-11-29 02:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("URLsub", "0012_alter_urlsub_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="urlsub",
            name="slug",
            field=models.SlugField(
                default="default-slug-value", max_length=200, unique=True
            ),
        ),
    ]
