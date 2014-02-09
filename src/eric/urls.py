from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()


_INVITE_PATTERNS = patterns(
    "eric.views",

    url(r"^$", "start_app", name="app_start"),
    url(r"^update-invitee/$", "update_invitee", name="invitee_updating"),

    )


_MANAGEMENT_PATTERNS = patterns(
    "eric.views",

    url(r"^import/$", "import_invites", name="data_import"),
    url(r"^export/$", "export_data_as_csv", name="data_export"),
    url(r"^$", "view_manage_options", name="management_home"),

    )


urlpatterns = patterns(
    "eric.views",

    (r"^invites/(?P<invite_key>[A-Za-z]{20})/", include(_INVITE_PATTERNS)),
    (r"^manage/", include(_MANAGEMENT_PATTERNS)),

    url(r"^info/$", "view_info", name="info"),
    url(r"^$", "view_homepage", name="home"),

    url(r"^admin/", include(admin.site.urls)),

)

urlpatterns += patterns('',
    url(r'^envelope\/?$', TemplateView.as_view(template_name='envelope.html'), name="envelope"),
)
