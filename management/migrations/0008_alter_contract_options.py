# Generated by Django 4.2.1 on 2023-06-30 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0007_convertertranslator_timestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'ordering': ['-timestamp']},
        ),
    ]
