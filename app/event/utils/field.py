"""
    Custom django ORM fields
"""
import importlib
from typing import Type, Optional

from django.conf import settings
from django.core import validators
from django.db import models
from django.db.models import Field
from django.utils.translation import gettext_lazy as _

from ..utils.encryption import KeyManager
from ..utils.enum import BaseChoice


class EncryptedTextField(models.Field):
    """
    Encrypted text field. Saves the data as an encrypted value in the database.
    Decrypts it when reading from the database. (for Django 2+ only)

    This class makes use of the `utils.encryption.KeyManager` interface for functioning.
    key_manager is an optional keyword argument, defaulting to django.conf.settings.ENCRYPTED_FIELD_KEY_MANAGER

    Usage:

        >>> from django.db import models
        >>> from utils.encryption import MockKeyManager
        >>>
        >>> key_manager = MockKeyManager()
        >>> class MyModel(models.Model):
        >>>     secret = EncryptedTextField(null=False, blank=False, key_manager=key_manager)

    """
    description = _('Encrypted text')

    def __init__(self, *args, **kwargs):
        self._key_manager = kwargs.pop('key_manager', None) or settings.ENCRYPTED_FIELD_KEY_MANAGER  # type: KeyManager
        if self._key_manager and isinstance(self._key_manager, str):
            module_path, class_name = self._key_manager.rsplit('.', 1)
            self._key_manager = getattr(importlib.import_module(module_path), class_name)
            if self._key_manager:
                self._key_manager = self._key_manager()

        if not self._key_manager or not isinstance(self._key_manager, KeyManager):
            raise ValueError(
                'key_manager is required and should be an instance of utils.encryption.KeyManager. '
                'It can be supplied either by passing it as a keyword argument, or by setting the '
                'ENCRYPTED_FIELD_KEY_MANAGER django setting'
            )

        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'blob'

        if connection.settings_dict['ENGINE'] in \
                ('django.db.backends.postgresql_psycopg2', 'django.db.backends.postgresql'):
            return 'bytea'

        raise NotImplementedError(
            f"Backend '{connection.settings_dict['ENGINE']}' not supported by EncryptedTextField")

    def get_prep_value(self, value):
        return self._key_manager.encrypt(value)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def from_db_value(self, value, expression, connection, *args):  # pylint: disable=unused-argument
        """ Convert the value retrieved from the DB by decrypting it and returning """
        if value is None:
            return value

        # this memoryview -> bytes conversion may not be such a great idea for performance
        if isinstance(value, memoryview):
            value = value.tobytes()

        return self._key_manager.decrypt(value)


class PrefixedIdField(models.TextField):
    """
        Creates Random Auto Generated Text prefixed with <prefix> param
        Max length can be upto 100. Prefix length is considered in Max Length
        Raises ValueError if key_length + prefix is greater than 100.
    """
    description = _("Random Auto Generated String max length upto 100")

    _DEFAULT_KEY_LENGTH = 12
    _MIN_PREFIXED_KEY_LENGTH = 16
    _MAX_LENGTH = 100

    key_length = None

    DEFAULT_PREFIX = '__base__'

    def __init__(self, prefix, key_length=_DEFAULT_KEY_LENGTH, **kwargs):
        self.prefix = prefix
        if not self.prefix:
            raise ValueError(f'Prefix is mandatory field: {self}')

        self.key_length = int(key_length or PrefixedIdField._DEFAULT_KEY_LENGTH)

        prefixed_key_length = self.key_length + len(prefix) + 1

        if prefixed_key_length < PrefixedIdField._MIN_PREFIXED_KEY_LENGTH:
            self.key_length += (PrefixedIdField._MIN_PREFIXED_KEY_LENGTH - prefixed_key_length)

        if self.key_length > self._MAX_LENGTH:
            raise ValueError('Maximum supported length is upto 100.')
        super(PrefixedIdField, self).__init__(max_length=self._MAX_LENGTH, blank=False, **kwargs)

    def deconstruct(self):
        _id, cls, args, kwargs = super(PrefixedIdField, self).deconstruct()
        del kwargs['max_length']
        kwargs['prefix'] = self.prefix
        return _id, cls, args, kwargs

    def db_type(self, connection):
        if self.prefix == PrefixedIdField.DEFAULT_PREFIX:
            raise ValueError(f'Prefix is not set: {self}')

        return "text default ('%s_' || base_model_key_generator(%d))" % (self.prefix, self.key_length)

    def rel_db_type(self, connection):
        return 'text'

    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name, private_only=private_only)
        cls._meta.has_auto_field = True  # pylint: disable=protected-access
        cls._meta.auto_field = self  # pylint: disable=protected-access


class LowerCaseCharField(models.CharField):
    """
    Makes sure its content is always lower-case
    """

    def to_python(self, value):
        value = super().to_python(value)

        if value:
            return value.lower()

        return value


class UpperCaseCharField(models.CharField):
    """
    Makes sure its content is always upper-case
    """

    def to_python(self, value):
        value = super().to_python(value)

        if value:
            return value.upper()

        return value


class _BaseChoiceFieldMixin:
    """
    Enum column powered by `utils.enum.BaseChoice`.
    Alternative to having to use/hardcode string/int enums. This automatically
    takes care of conversion from the database str/int value to the Enum object value, and vice versa.

    Usage:

        >>> from django.db import models
        >>> class Weekday(BaseChoice):
        >>>     MONDAY = ("mon", "Monday blues")
        >>>     TUESDAY = ("tues", "Meh")
        >>>     WEDNESDAY = ("wed", "Halfway through!")
        >>>     THURSDAY = ("wed", "Almost there...")
        >>>     FRIDAY = ("fri", "Party!")
        >>>
        >>> class MyModel(models.Model):
        >>>     day = _BaseChoiceFieldMixin(null=False, blank=False, choices=Weekday)
    """

    def __init__(self, *args, **kwargs):
        self._choices_cls = kwargs.pop('choices')  # type: Type[BaseChoice]
        if not self._choices_cls \
                or not isinstance(self._choices_cls, type) \
                or not issubclass(self._choices_cls, BaseChoice):
            raise ValueError('choices is required and should a utils.enum.BaseChoice subclass')

        choices = [(member, member.message) for member in self._choices_cls]
        super().__init__(*args, choices=choices, **kwargs)

    def deconstruct(self):
        """
        Opposite of init, required to deconstruct the field.
        Django Migrations will break without this method.
        """
        name, path, args, kwargs = super().deconstruct()
        # choices that was originally passed in was BaseChoice subclass, not list
        kwargs['choices'] = kwargs['choices'][0][0].__class__
        return name, path, args, kwargs

    def to_python(self, value):
        """ Convert object to python """
        if isinstance(value, BaseChoice) or value is None:
            return value

        ret = self._choices_cls.from_ident(value)
        return ret

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def from_db_value(
            self, value, expression, connection, *args) -> Optional[BaseChoice]:  # pylint: disable=unused-argument
        """ Convert the value retrieved from the DB into a BaseChoice enum """
        if value is None:
            return value

        ret = self._choices_cls.from_ident(value)
        return ret

    def get_prep_value(self, value: BaseChoice):
        """ Prepare value for saving to the database """
        value = super().get_prep_value(value)
        return None if value is None else value.ident

    def value_to_string(self, obj):
        """
        Required to serialize the value into string format
        """
        value = self.value_from_object(obj)
        value = self.get_prep_value(value)
        return '' if value is None else str(value)


class CharChoiceField(_BaseChoiceFieldMixin, models.CharField):
    """
    CHAR enum column powered by `utils.enum.BaseChoice`.

    See `_BaseChoiceFieldMixin` docstring for detailed usage docs.
    """
    description = _('Char Choice')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # BaseChoice objects do not have a __len__() protocol, so the MaxLengthValidator
        # that's added by CharField will raise an Exception. We work around it by hijacking the
        # .clean() method and make it work with BaseChoice as well
        for val in self.validators:
            if isinstance(val, validators.MaxLengthValidator):
                val.clean = lambda x: (len(x.ident) if isinstance(x, self._choices_cls) else len(x))


class TextChoiceField(_BaseChoiceFieldMixin, models.TextField):
    """
    TEXT enum column powered by `utils.enum.BaseChoice`.

    See `_BaseChoiceFieldMixin` docstring for detailed usage docs.
    """
    description = _('Text Choice')


class IntegerChoiceField(_BaseChoiceFieldMixin, models.IntegerField):
    """
    INTEGER enum column powered by `utils.enum.BaseChoice`.

    See `_BaseChoiceFieldMixin` docstring for detailed usage docs.
    """
    description = _('Integer Choice')

    def get_prep_value(self, value: BaseChoice):
        """ Prepare value for saving to the database """
        # skip the _BaseChoiceFieldMixin and IntegerField super().get_prep_value() calls,
        # instead go ahead and directly call Field.get_prep_value(). We need that in order
        # so support Promise values
        value = Field.get_prep_value(self, value)
        value = self.to_python(value)
        return None if value is None else value.ident
