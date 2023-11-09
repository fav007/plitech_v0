# Generated by Django 4.2.4 on 2023-11-04 13:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("expense", "0005_expense_created_at_expense_updated_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="Jirama",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("index", models.IntegerField()),
                ("date", models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
