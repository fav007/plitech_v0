# Generated by Django 4.2.4 on 2023-10-03 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("entry", "0005_be_line_alter_be_customers_alter_be_time_entry_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="be_line",
            name="be",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="be_lines",
                to="entry.be",
            ),
        ),
    ]
