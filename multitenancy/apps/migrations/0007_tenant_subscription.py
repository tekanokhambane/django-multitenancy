# Generated by Django 3.2.12 on 2022-11-12 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
        ('apps', '0006_alter_tenant_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='subscription',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subscriptions.subscription'),
        ),
    ]
