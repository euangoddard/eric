from functools import wraps

from django.http.response import HttpResponseForbidden
from django.template.response import TemplateResponse

from eric import INVITE_SESSION_KEY
from eric.models import Invite

def require_invite_in_session(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        invite_key = request.session.get(INVITE_SESSION_KEY)
        
        invites = Invite.objects.filter(key=invite_key)
        if invites.exists():
            response = view(request, *args, **kwargs)
        else:
            response = _get_forbidden_rsponse(request)
        
        return response
    
    return wrapper


def _get_forbidden_rsponse(request):
    response = TemplateResponse(request, "403.html")
    response.status_code = HttpResponseForbidden.status_code
    return response
