# Generated by Django 4.2.4 on 2023-10-13 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expense", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="total",
            field=models.IntegerField(verbose_name="Total Amount"),
        ),
    ]
