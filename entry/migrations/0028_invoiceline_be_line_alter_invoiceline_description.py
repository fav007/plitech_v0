# Generated by Django 4.1 on 2023-10-12 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0027_alter_be_line_sm_eqv'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceline',
            name='be_line',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='entry.be_line'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
