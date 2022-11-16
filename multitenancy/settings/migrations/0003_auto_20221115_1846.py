# Generated by Django 3.2.12 on 2022-11-15 16:46

from django.db import migrations, models
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20221115_0817'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Address'},
        ),
        migrations.RemoveField(
            model_name='generalinfo',
            name='phone',
        ),
        migrations.AddField(
            model_name='address',
            name='address_line_1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='postal_code',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Post/Zip-code'),
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='State/Province'),
        ),
        migrations.AddField(
            model_name='generalinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='generalinfo',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.AddField(
            model_name='generalinfo',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
