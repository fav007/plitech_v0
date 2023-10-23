# Generated by Django 4.2.4 on 2023-10-23 04:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("entry", "0033_banknote_created_at_banknote_updated_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="be_line",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="be_line",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="invoiceline",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="invoiceline",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
