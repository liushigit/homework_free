from django.db.models.fields import CharField
from django.utils.translation import ugettext_lazy as _

from general_tools_app.forms.fields import CNMobileNumberField


class MobileNumberField(CharField):

    description = _("China mobile number")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 11
        super(MobileNumberField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': CNMobileNumberField}
        defaults.update(kwargs)
        return super(MobileNumberField, self).formfield(**defaults)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^general_tools_app\.models\.fields\.MobileNumberField"])