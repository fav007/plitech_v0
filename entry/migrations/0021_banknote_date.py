# Generated by Django 4.1.7 on 2023-10-10 16:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0020_banknote'),
    ]

    operations = [
        migrations.AddField(
            model_name='banknote',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]