# Generated by Django 4.2.1 on 2023-06-10 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="management",
            old_name="rent_security",
            new_name="required_amount",
        ),
        migrations.RenameField(
            model_name="management",
            old_name="rent_security_type",
            new_name="security_type_code",
        ),
    ]
