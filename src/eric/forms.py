import csv

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.forms.fields import FileField
from django.forms.forms import Form
from django.forms.models import ModelForm

from eric.models import Invitee


class InviteeForm(ModelForm):
    
    class Meta:
        model = Invitee
        fields = ("is_attending", "special_requirements")


class InviteImportForm(Form):
    
    csv_file = FileField()
    
    def clean_csv_file(self):
        csv_upload = self.cleaned_data["csv_file"]
        
        try:
            csv_reader = csv.reader(csv_upload)
            csv_data = list(csv_reader)
        except IOError as exc:
            raise ValidationError(u"Could not read CSV file: {}".format(exc))
        except (ValueError, TypeError) as exc:
            raise ValidationError(u"CSV data was corrupted: {}".format(exc))
        
        self._validate_all_email_addresses_valid(csv_data)
        return csv_data
    
    @staticmethod
    def _validate_all_email_addresses_valid(data):
        try:
            email_addresses = zip(*data)[0]
        except IndexError:
            raise ValidationError(u"CSV file cannot be empty!")
        
        for email_address in email_addresses:
            error_message = \
                u"'{}' is not a valid email address".format(email_address)
            validator = EmailValidator(message=error_message)
            validator(email_address)
