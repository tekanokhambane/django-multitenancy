# include these urls instead of urls.py if you are using the WSGI + Django middlewares
# to set request.team, manually hooking up List/Create views as well as the accept/reject

from django.conf.urls import url

from . import views

app_name = "pinax_teams"


urlpatterns = [
    # team specific
    url(r"^detail/$", views.team_detail, name="team_detail"),
    url(r"^join/$", views.team_join, name="team_join"),
    url(r"^leave/$", views.team_leave, name="team_leave"),
    url(r"^apply/$", views.team_apply, name="team_apply"),
    url(r"^edit/$", views.team_update, name="team_edit"),
    url(r"^manage/$", views.TeamManageView.as_view(), name="team_manage"),
    url(r"^ac/users-to-invite/$", views.autocomplete_users, name="team_autocomplete_users"),  # noqa
    url(r"^invite-user/$", views.TeamInviteView.as_view(), name="team_invite"),
    url(r"^members/(?P<pk>\d+)/revoke-invite/$", views.team_member_revoke_invite, name="team_member_revoke_invite"),  # noqa
    url(r"^members/(?P<pk>\d+)/resend-invite/$", views.team_member_resend_invite, name="team_member_resend_invite"),  # noqa
    url(r"^members/(?P<pk>\d+)/promote/$", views.team_member_promote, name="team_member_promote"),  # noqa
    url(r"^members/(?P<pk>\d+)/demote/$", views.team_member_demote, name="team_member_demote"),  # noqa
    url(r"^members/(?P<pk>\d+)/remove/$", views.team_member_remove, name="team_member_remove"),  # noqa
]
