from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.options import TabularInline
from django.contrib.admin.sites import site

from eric.models import Invite
from eric.models import Invitee


class InviteeAdmin(TabularInline):
    
    model = Invitee


class InviteAdmin(ModelAdmin):
    
    list_display = ("key", "email", "invitees")
    
    inlines = (InviteeAdmin, )
    
    def invitees(self, invite):
        invitee_names = invite.invitees.values_list("name", flat=True)
        if invitee_names:
            label = u", ".join(invitee_names)
        else:
            label = u"(No invitees)"
        return label


site.register(Invite, InviteAdmin)
