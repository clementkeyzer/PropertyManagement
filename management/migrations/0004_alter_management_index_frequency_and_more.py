# Generated by Django 4.2.1 on 2023-06-22 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0003_alter_management_charge_frequency_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="management",
            name="index_frequency",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="management",
            name="term_frequency",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
