# Generated by Django 3.2.12 on 2023-08-25 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0014_subscription_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='name',
            field=models.CharField(choices=[('personal', 'personal'), ('freemium', 'freemium'), ('premium', 'premium'), ('business', 'business')], max_length=250, unique=True),
        ),
    ]
