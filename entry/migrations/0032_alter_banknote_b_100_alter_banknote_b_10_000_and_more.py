# Generated by Django 4.2.4 on 2023-10-18 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("entry", "0031_alter_invoice_metal_scrap"),
    ]

    operations = [
        migrations.AlterField(
            model_name="banknote",
            name="b_100",
            field=models.IntegerField(default=0, verbose_name="100 MGA"),
        ),
        migrations.AlterField(
            model_name="banknote",
            name="b_10_000",
            field=models.IntegerField(default=0, verbose_name="10 000 MGA"),
        ),
        migrations.AlterField(
            model_name="banknote",
            name="b_1_000",
            field=models.IntegerField(default=0, verbose_name="1 000 MGA"),
        ),
        migrations.AlterField(
            model_name="banknote",
            name="b_200",
            field=models.IntegerField(default=0, verbose_name="200 MGA"),
        ),
        migrations.AlterField(
            model_name="banknote",
            name="b_20_000",
            field=models.IntegerField(default=0, verbose_name="20 000 MGA"),
        ),
        migrations.AlterField(
            model_name="banknote",
            name="b_2_000",
            field=models.IntegerField(default=0, verbose_name="2 000 MGA"),
        ),
        migrations.AlterField(
            model_name="banknote",
            name="b_500",
            field=models.IntegerField(default=0, verbose_name="500 MGA"),
        ),
        migrations.AlterField(
            model_name="banknote",
            name="b_5_000",
            field=models.IntegerField(default=0, verbose_name="5 000 MGA"),
        ),
    ]
