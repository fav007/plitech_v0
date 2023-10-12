# Generated by Django 4.2.4 on 2023-10-12 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("entry", "0029_invoice_metal_scrap"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="metal_scrap",
            field=models.DecimalField(
                decimal_places=5, default=0, max_digits=5, verbose_name="Metal SCRAP"
            ),
        ),
    ]
