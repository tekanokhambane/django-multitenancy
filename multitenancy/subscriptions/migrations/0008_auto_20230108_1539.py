# Generated by Django 3.2.12 on 2023-01-08 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_auto_20230108_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscription_duration',
            field=models.IntegerField(default=30),
        ),
    ]