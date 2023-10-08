# Generated by Django 4.2.5 on 2023-10-07 04:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_alter_blogfullrecommend_tags_alter_post_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogfullrecommend",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="BlogFullRecommend_image/"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="Post_image/"),
        ),
    ]