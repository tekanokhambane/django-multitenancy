# Generated by Django 3.2.12 on 2023-01-07 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0006_auto_20230107_1742'),
        ('apps', '0011_auto_20230101_0650'),
    ]

    operations = [
        migrations.RenameField(
            model_name='domain',
            old_name='has_custom',
            new_name='is_custom',
        ),
        migrations.AddField(
            model_name='tenant',
            name='subscription',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenants', to='subscriptions.subscription'),
        ),
        migrations.AddField(
            model_name='tenant',
            name='trail_duration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tenants', to='subscriptions.plan'),
        ),
    ]
