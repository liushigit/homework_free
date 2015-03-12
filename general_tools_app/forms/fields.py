# coding:utf-8
import re
from django.forms.fields import CharField
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _


cn_mobile_digits = re.compile(r'^\d{11}$')

class CNMobileNumberField(CharField):
    default_error_messages = {
        'invalid': _('Invalid phone number'),
    }


    def clean(self, value):
        super(CNMobileNumberField, self).clean(value)

        if value in EMPTY_VALUES:
            return u''
        
        match = cn_mobile_digits.match(value)

        if match:
            return value

        raise ValidationError(self.error_messages['invalid'])