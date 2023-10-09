# Generated by Django 4.2.4 on 2023-10-07 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("entry", "0015_invoice_be_invoiceline_invoice"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoiceline",
            name="invoice",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="invoice_line",
                to="entry.invoice",
            ),
        ),
    ]