# Generated by Django 4.2.1 on 2023-07-30 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_alter_managementrule_gross_area_then_net_area_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='managementrule',
            name='vacant_required',
            field=models.BooleanField(default=True),
        ),
    ]
