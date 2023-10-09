# Generated by Django 4.1.7 on 2023-10-07 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0010_invoiceline_invoice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoiceline',
            old_name='up',
            new_name='unit_price',
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='description',
            field=models.CharField(default='now', max_length=200),
            preserve_default=False,
        ),
    ]