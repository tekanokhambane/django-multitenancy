# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-11 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    # run_before = ("helpdesk", "0028_kbitem_team")

    dependencies = [
        ("multitenancy_teams", "0003_auto_20170416_1752"),
    ]

    operations = [
        migrations.AlterField(
            model_name="membership",
            name="state",
            field=models.CharField(
                choices=[
                    ("applied", "applied"),
                    ("invited", "invited"),
                    ("declined", "declined"),
                    ("rejected", "rejected"),
                    ("accepted", "accepted"),
                    ("waitlisted", "waitlisted"),
                    ("auto-joined", "auto joined"),
                ],
                max_length=20,
                verbose_name="state",
            ),
        ),
        migrations.AlterField(
            model_name="simplemembership",
            name="state",
            field=models.CharField(
                choices=[
                    ("applied", "applied"),
                    ("invited", "invited"),
                    ("declined", "declined"),
                    ("rejected", "rejected"),
                    ("accepted", "accepted"),
                    ("waitlisted", "waitlisted"),
                    ("auto-joined", "auto joined"),
                ],
                max_length=20,
                verbose_name="state",
            ),
        ),
    ]
