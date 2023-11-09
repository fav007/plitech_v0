# Generated by Django 4.2.4 on 2023-11-04 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0009_customers_created_at_customers_updated_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customers_t",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "title",
                    models.CharField(
                        choices=[("M.", "Monsieur"), ("Mme", "Madame")], max_length=3
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
                ("company", models.CharField(max_length=200)),
                ("contact", models.CharField(max_length=10)),
                ("location", models.CharField(max_length=100)),
            ],
        ),
    ]
