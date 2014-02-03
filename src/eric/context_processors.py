from datetime import datetime

from eric import INVITE_SESSION_KEY
from eric.models import Invite


def get_constants(request):
    
    return {
        "NAMING_DAY_START_TIME": datetime(2014, 5, 10, 13)
        }


def get_current_invite(request):
    invite_key = request.session.get(INVITE_SESSION_KEY)
    try:
        invite = Invite.objects.get(key=invite_key)
    except Invite.DoesNotExist:
        invite = None
    return {
        "current_invite": invite,
        }
