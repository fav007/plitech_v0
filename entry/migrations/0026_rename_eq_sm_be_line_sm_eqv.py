# Generated by Django 4.1.7 on 2023-10-11 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0025_be_line_eq_sm_alter_invoice_discount_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='be_line',
            old_name='eq_sm',
            new_name='sm_eqv',
        ),
    ]
