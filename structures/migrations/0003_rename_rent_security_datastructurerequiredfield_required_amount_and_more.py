# Generated by Django 4.2.1 on 2023-06-10 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("structures", "0002_alter_datastructure_date_of_lease_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="datastructurerequiredfield",
            old_name="rent_security",
            new_name="required_amount",
        ),
        migrations.RenameField(
            model_name="datastructurerequiredfield",
            old_name="rent_security_type",
            new_name="security_type_code",
        ),
        migrations.RemoveField(
            model_name="datastructure",
            name="rent_security",
        ),
        migrations.RemoveField(
            model_name="datastructure",
            name="rent_security_type",
        ),
        migrations.AddField(
            model_name="datastructure",
            name="required_amount",
            field=models.CharField(
                blank=True, default="required_amount", max_length=250, null=True
            ),
        ),
        migrations.AddField(
            model_name="datastructure",
            name="security_type_code",
            field=models.CharField(
                blank=True, default="security_type_code", max_length=250, null=True
            ),
        ),
    ]
