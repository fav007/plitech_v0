# Generated by Django 4.1.7 on 2023-10-07 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0007_be_line_length_be_line_width_alter_be_line_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='be_line',
            name='owner',
            field=models.CharField(choices=[('Client', 'Client'), ('Hanitra', 'Hanitra'), ('Tojo', 'Tojo')], default='Client', max_length=10),
        ),
    ]
