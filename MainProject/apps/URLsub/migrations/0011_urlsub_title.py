# Generated by Django 4.2.5 on 2023-11-27 17:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("URLsub", "0010_remove_urlsub_recommendations_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="urlsub",
            name="title",
            field=models.TextField(default="YourDefaultValueHere"),
        ),
    ]
