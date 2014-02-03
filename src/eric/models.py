from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields import NullBooleanField
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey

from eric.fields import AlphaUniqueField
from django.db.models.fields import EmailField


class Invite(Model):
    
    key = AlphaUniqueField(primary_key=True, editable=False)
    
    email = EmailField()
    
    def __unicode__(self):
        return self.key
    
    @property
    def is_complete(self):
        unconfirmed_invitees = self.invitees.filter(is_attending__isnull=True)
        return not unconfirmed_invitees.exists()
        


class Invitee(Model):
    
    invite = ForeignKey(Invite, related_name="invitees")
    
    name = CharField(max_length=30)
    
    is_attending = NullBooleanField()
    
    special_requirements = TextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name
