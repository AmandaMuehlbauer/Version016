# Generated by Django 4.2.5 on 2023-11-03 03:15

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):
    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
        ("URLsub", "0006_alter_urlsub_options_rename_username_urlsub_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="urlsub",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
