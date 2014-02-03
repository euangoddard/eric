import csv
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView

from eric import INVITE_SESSION_KEY
from eric.decorators import require_invite_in_session
from eric.forms import InviteImportForm
from eric.forms import InviteeForm
from eric.models import Invite
from eric.models import Invitee


_HTTP_METHOD_POST = "POST"


_INVITEE_NAME_MAX_LENGTH = Invitee._meta.get_field("name").max_length


def start_app(request, invite_key):
    invite = get_object_or_404(Invite, key=invite_key)
    request.session[INVITE_SESSION_KEY] = invite.key
    response = redirect("home")
    return response


class _HomePageView(TemplateView):

    template_name = "home.html"

view_homepage = require_invite_in_session(_HomePageView.as_view())


class _InfoPageView(TemplateView):

    template_name = "info.html"

view_info = require_invite_in_session(_InfoPageView.as_view())


@require_POST
@require_invite_in_session
def update_invitee(request, invite_key):
    if invite_key != request.session[INVITE_SESSION_KEY]:
        return HttpResponseForbidden("You cannot update that invite")
    
    invitee_data = json.loads(request.body)
    print invitee_data
    invitee_id = invitee_data.get("id")
    if not invitee_id:
        return HttpResponseBadRequest("Invitee primary key is missing!")
    
    try:
        invitee = Invitee.objects.get(pk=invitee_id, invite__pk=invite_key)
    except Invitee.DoesNotExist:
        response = HttpResponseBadRequest(
            "Invitee matching primary key cannot be found",
            )
    else:
        form = InviteeForm(invitee_data, instance=invitee)
        if form.is_valid():
            form.save()
            response_data = {"is_invite_complete": invitee.invite.is_complete}
            response = HttpResponse(json.dumps(response_data))
        else:
            response = HttpResponseBadRequest("Field missing")
    
    return response


class _ManagePageView(TemplateView):
    
    template_name = "manage.html"

view_manage_options = \
    user_passes_test(lambda user: user.is_staff)(_ManagePageView.as_view())


@login_required
@user_passes_test(lambda user: user.is_staff)
def export_data_as_csv(request):
    rows = [["Email", "Name", "Invite URL"]]
    for invite in Invite.objects.prefetch_related("invitees"):
        invite_url = reverse("app_start", kwargs={"invite_key": invite.key})
        invite_name = invite.invitees.all()[0].name
        row = [
            invite.email.encode("utf8"),
            invite_name.encode("utf8"),
            request.build_absolute_uri(invite_url).encode("utf8"),
            ]
        rows.append(row)
    
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=invites.csv"
    csv_writer = csv.writer(response)
    csv_writer.writerows(rows)
    return response


@login_required
@user_passes_test(lambda user: user.is_staff)
def import_invites(request):
    if request.method == _HTTP_METHOD_POST:
        form_data = (request.POST, request.FILES)
    else:
        form_data = ()
    
    form = InviteImportForm(*form_data)
    
    if request.method == _HTTP_METHOD_POST and form.is_valid():
        csv_data = form.cleaned_data["csv_file"]
        invites_created = _create_invites_from_csv_data(csv_data)
        messages.info(request, u"Created {} invites".format(invites_created))
        response = redirect("data_import")
    else:
        response = TemplateResponse(request, "import.html", {"form": form})
    
    return response


def _create_invites_from_csv_data(csv_data):
    invites_created = 0
    for row in csv_data:
        email_address = row[0]
        invitee_names = row[1:]
        invite = Invite.objects.create(email=email_address)
        _add_invitees_to_invite(invite, invitee_names)
        invites_created += 1
    
    return invites_created


def _add_invitees_to_invite(invite, invitee_names):
    for invitee_name in invitee_names:
        invite.invitees.create(name=invitee_name[:_INVITEE_NAME_MAX_LENGTH])