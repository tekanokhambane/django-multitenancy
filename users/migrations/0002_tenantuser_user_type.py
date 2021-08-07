# Generated by Django 3.1.13 on 2021-08-04 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenantuser',
            name='user_type',
            field=models.CharField(choices=[('1', 'HOD'), ('2', 'Staff'), ('3', 'Customer'), ('4', 'AppUser')], default=1, max_length=10),
        ),
    ]
