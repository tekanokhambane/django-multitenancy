# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-03 21:40
from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("multitenancy_invitations", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("multitenancy_teams", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SimpleMembership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            (b"applied", "applied"),
                            (b"invited", "invited"),
                            (b"declined", "declined"),
                            (b"rejected", "rejected"),
                            (b"accepted", "accepted"),
                            (b"auto-joined", "auto joined"),
                        ],
                        max_length=20,
                        verbose_name="state",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            (b"member", "member"),
                            (b"manager", "manager"),
                            (b"owner", "owner"),
                        ],
                        default=b"member",
                        max_length=20,
                        verbose_name="role",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="created"
                    ),
                ),
                (
                    "invite",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="simple_memberships",
                        to="multitenancy_invitations.JoinInvitation",
                        verbose_name="invite",
                    ),
                ),
            ],
            options={
                "verbose_name": "Simple Membership",
                "verbose_name_plural": "Simple Memberships",
            },
        ),
        migrations.CreateModel(
            name="SimpleTeam",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "member_access",
                    models.CharField(
                        choices=[
                            (b"open", "open"),
                            (b"application", "by application"),
                            (b"invitation", "by invitation"),
                        ],
                        max_length=20,
                        verbose_name="member access",
                    ),
                ),
                (
                    "manager_access",
                    models.CharField(
                        choices=[
                            (b"add someone", "add someone"),
                            (b"invite someone", "invite someone"),
                        ],
                        max_length=20,
                        verbose_name="manager access",
                    ),
                ),
            ],
            options={
                "verbose_name": "Simple Team",
                "verbose_name_plural": "Simple Teams",
            },
        ),
        migrations.AlterModelOptions(
            name="membership",
            options={
                "verbose_name": "Membership",
                "verbose_name_plural": "Memberships",
            },
        ),
        migrations.AddField(
            model_name="simplemembership",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="memberships",
                to="multitenancy_teams.SimpleTeam",
                verbose_name="team",
            ),
        ),
        migrations.AddField(
            model_name="simplemembership",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="simple_memberships",
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="simplemembership",
            unique_together=set([("team", "user", "invite")]),
        ),
    ]
