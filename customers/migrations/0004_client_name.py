# Generated by Django 3.1.13 on 2021-09-28 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20210729_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='name',
            field=models.CharField(default='Name', max_length=200),
        ),
    ]
