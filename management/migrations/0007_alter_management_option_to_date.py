# Generated by Django 4.2.1 on 2023-05-29 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0006_managementrule_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="management",
            name="option_to_date",
            field=models.DateField(blank=True, max_length=240, null=True),
        ),
    ]