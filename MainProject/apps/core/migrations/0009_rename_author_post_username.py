# Generated by Django 4.1.6 on 2023-08-26 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_comment_username"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post", old_name="author", new_name="username",
        ),
    ]
