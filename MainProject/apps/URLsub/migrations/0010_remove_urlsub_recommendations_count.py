# Generated by Django 4.2.5 on 2023-11-03 17:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("URLsub", "0009_alter_urlsub_unique_together"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="urlsub",
            name="recommendations_count",
        ),
    ]
