# Generated by Django 3.1.13 on 2021-08-12 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210812_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydetails',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]