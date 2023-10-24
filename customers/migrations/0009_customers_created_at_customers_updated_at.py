# Generated by Django 4.2.4 on 2023-10-22 09:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0008_customers_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="customers",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="customers",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]