# Generated by Django 4.2.1 on 2023-05-26 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contract",
            name="status",
            field=models.CharField(
                choices=[("PENDING", "PENDING"), ("SUCCESS", "SUCCESS")],
                default="PENDING",
                max_length=250,
            ),
        ),
    ]