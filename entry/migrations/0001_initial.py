# Generated by Django 4.2.5 on 2023-09-26 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0004_delete_be'),
    ]

    operations = [
        migrations.CreateModel(
            name='BE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entry', models.DateField(auto_now_add=True)),
                ('time_entry', models.TimeField(auto_now_add=True)),
                ('customers', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customers.customers')),
            ],
        ),
    ]
