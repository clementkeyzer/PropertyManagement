# Generated by Django 4.2.1 on 2023-08-21 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0013_optioncode_rentsecuritydepositcode_field_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentsecuritydepositcode',
            name='field_name',
        ),
    ]
