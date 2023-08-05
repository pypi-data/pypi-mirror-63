import shortuuid
import django.db.models
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.utils.translation import gettext_lazy as _


class NativeShortUUIDFormField(CharField):
    default_error_messages = {
        'invalid': _('Enter a valid ShortUUID.'),
    }

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        try:
            shortuuid.decode(value)
        except ValueError:
            raise ValidationError(self.error_messages['invalid'], code='invalid')
        return value


class NativeShortUUIDField(django.db.models.UUIDField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return shortuuid.encode(value)

    def to_python(self, value):
        if value is None:
            return value

        return super().to_python(shortuuid.decode(value))

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': NativeShortUUIDFormField,
            **kwargs,
        })
