import json

from django.template.base import Library
from django.utils.html import escape

register = Library()


@register.simple_tag
def serialize_invite(invite):
    invitee_data = []
    for invitee_values in invite.invitees.values():
        invitee_data.append(invitee_values)
    
    invite_data = {
        "key": invite.key,
        "is_complete": invite.is_complete,
        "invitees": invitee_data,
        }
    
    return escape(json.dumps(invite_data))
