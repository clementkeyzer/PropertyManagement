# Generated by Django 4.2.1 on 2023-08-21 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structures', '0002_datastructurerequiredfield_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datastructure',
            name='type_code',
        ),
        migrations.AddField(
            model_name='datastructure',
            name='option_type_code',
            field=models.CharField(blank=True, default='option_type_code', max_length=250, null=True),
        ),
    ]