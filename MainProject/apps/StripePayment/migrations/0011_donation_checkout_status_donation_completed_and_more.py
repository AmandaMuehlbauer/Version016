# Generated by Django 4.2.5 on 2024-01-25 00:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("StripePayment", "0010_subscription_is_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="checkout_status",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="donation",
            name="completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="subscription",
            name="checkout_status",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="subscription",
            name="completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="subscription_plan_id",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
