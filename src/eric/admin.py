from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.options import TabularInline
from django.contrib.admin.sites import site

from eric.models import Invite
from eric.models import Invitee


class InviteeInlineAdmin(TabularInline):
    
    model = Invitee


class InviteAdmin(ModelAdmin):
    
    list_display = ("key", "email", "invitees")
    
    inlines = (InviteeInlineAdmin, )
    
    def invitees(self, invite):
        invitee_names = invite.invitees.values_list("name", flat=True)
        if invitee_names:
            label = u", ".join(invitee_names)
        else:
            label = u"(No invitees)"
        return label


class InviteeAdmin(ModelAdmin):
    
    list_display = (
        "invite",
        "name",
        "is_attending",
        "special_requirements",
    )
    
    list_filter = ("is_attending", )


site.register(Invite, InviteAdmin)
site.register(Invitee, InviteeAdmin)
