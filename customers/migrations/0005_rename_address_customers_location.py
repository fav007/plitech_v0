# Generated by Django 4.2.4 on 2023-10-03 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0004_delete_be"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customers",
            old_name="address",
            new_name="location",
        ),
    ]