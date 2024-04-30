from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from reversion.admin import VersionAdmin

from .hooks import hookset
from .models import Membership, Team


def members_count(obj):
    return obj.memberships.count()


members_count.short_description = _("Members Count")


admin.site.register(
    Team,
    list_display=["name", "member_access", "manager_access", members_count, "creator"],
    fields=[
        "name",
        "slug",
        "avatar",
        "description",
        "member_access",
        "manager_access",
        "creator"
    ],
    prepopulated_fields={"slug": ("name",)},
    raw_id_fields=["creator"]
)


class MembershipAdmin(VersionAdmin):
    raw_id_fields = ["user"]
    list_display = ["team", "user", "state", "role"]
    list_filter = ["team"]
    search_fields = hookset.membership_search_fields


admin.site.register(Membership, MembershipAdmin)
