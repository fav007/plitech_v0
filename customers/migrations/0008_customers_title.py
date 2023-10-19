# Generated by Django 4.2.4 on 2023-10-13 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0007_alter_customers_company_alter_customers_contact_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customers",
            name="title",
            field=models.CharField(
                choices=[("M.", "Monsieur"), ("Mme", "Madame")],
                default="M.",
                max_length=3,
            ),
            preserve_default=False,
        ),
    ]