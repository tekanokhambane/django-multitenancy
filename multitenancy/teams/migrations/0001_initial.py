# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import multitenancy.teams.models


class Migration(migrations.Migration):

    dependencies = [
        ("multitenancy_invitations", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Membership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        max_length=20,
                        verbose_name="state",
                        choices=[
                            (b"applied", "applied"),
                            (b"invited", "invited"),
                            (b"declined", "declined"),
                            (b"rejected", "rejected"),
                            (b"accepted", "accepted"),
                            (b"auto-joined", "auto joined"),
                        ],
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        default=b"member",
                        max_length=20,
                        verbose_name="role",
                        choices=[
                            (b"member", "member"),
                            (b"manager", "manager"),
                            (b"owner", "owner"),
                        ],
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
                        related_name="memberships",
                        verbose_name="invite",
                        blank=True,
                        to="multitenancy_invitations.JoinInvitation",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Team",
                "verbose_name_plural": "Teams",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("slug", models.SlugField(unique=True)),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "avatar",
                    models.ImageField(
                        upload_to=multitenancy.teams.models.avatar_upload,
                        verbose_name="avatar",
                        blank=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(verbose_name="description", blank=True),
                ),
                (
                    "member_access",
                    models.CharField(
                        max_length=20,
                        verbose_name="member access",
                        choices=[
                            (b"open", "open"),
                            (b"application", "by application"),
                            (b"invitation", "by invitation"),
                        ],
                    ),
                ),
                (
                    "manager_access",
                    models.CharField(
                        max_length=20,
                        verbose_name="manager access",
                        choices=[
                            (b"add someone", "add someone"),
                            (b"invite someone", "invite someone"),
                        ],
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="created",
                        editable=False,
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        related_name="teams_created",
                        verbose_name="creator",
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "verbose_name": "Team",
                "verbose_name_plural": "Teams",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="membership",
            name="team",
            field=models.ForeignKey(
                related_name="memberships",
                verbose_name="team",
                to="multitenancy_teams.Team",
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="membership",
            name="user",
            field=models.ForeignKey(
                related_name="memberships",
                verbose_name="user",
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="membership",
            unique_together=set([("team", "user", "invite")]),
        ),
    ]
