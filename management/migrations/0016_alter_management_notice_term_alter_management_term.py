# Generated by Django 4.2.1 on 2023-11-09 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0015_chargefrequencycode_currencycode_indexfrequency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='management',
            name='notice_term',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='management',
            name='term',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
