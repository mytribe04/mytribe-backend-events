"""
More useful enum constructs
"""

import enum
from typing import Dict, List, Tuple, Union


class Choice:
    """ Wrapper for tuple to satisfy pylint """
    def __init__(self, ident: Union[str, int], message: str):
        self.ident = ident
        self.message = message


class BaseChoice(enum.Enum):
    """
    Base class for creating choice enumerations

    Usage:

    >>> class Weekday(BaseChoice):
    >>>     MONDAY = Choice("mon", "Monday blues")  # either Choice
    >>>     TUESDAY = ("tues", "Meh")               # or normal tuples
    >>>     WEDNESDAY = ("wed", "Halfway through!")
    >>>     THURSDAY = ("wed", "Almost there...")
    >>>     FRIDAY = ("fri", "Party!")
    >>>
    >>> Weekday.MONDAY.value  # returns 'mon'
    >>> Weekday.MONDAY.ident  # returns 'mon'
    >>> Weekday.MONDAY.message  # returns 'Monday blues'
    >>> Weekday.from_ident('mon')  # returns Weekday.MONDAY
    >>> Weekday.from_name('MONDAY')  # returns Weekday.MONDAY
    >>>

    You can also override __new__ to use more complex declaration logic
    """

    # noinspection SpellCheckingInspection
    def __new__(cls, *args, **kwds):  # pylint: disable=unused-argument
        if len(args) == 1:
            choice: Choice = args[0]
            ident, message = choice.ident, choice.message
        else:
            ident, message = args

        # prevent accidental re-use of enum ident
        existing = cls.as_ident_enum_dict()
        if ident in existing:
            raise ValueError(f"Attempted to re-use ident '{ident}', already in use at {existing[ident]}")

        obj = object.__new__(cls)
        obj._value_ = ident
        obj.ident = ident
        obj.message = message
        return obj

    @classmethod
    def as_tuples(cls) -> List[Tuple[object, str]]:
        """ Returns a list of (ident, message) tuples """
        return [(member.ident, member.message) for member in cls]

    @classmethod
    def as_filtered_tuples(cls, allowed_idents: List[object]):
        """ Returns a list of (ident, message) tuples, but only filtered to provided allow list """
        return [(member.ident, member.message) for member in cls
                if member.ident in allowed_idents]

    @classmethod
    def as_ident_enum_dict(cls) -> Dict[object, 'BaseChoice']:
        """ Returns a dict of ident: message key value pairs """
        return {member.ident: member for member in cls}

    @classmethod
    def as_ident_message_dict(cls) -> Dict[object, str]:
        """ Returns a dict of ident: message key value pairs """
        return {ident: member.message for ident, member in cls.as_ident_enum_dict().items()}

    @classmethod
    def from_name(cls, name: object) -> 'BaseChoice':
        """ Get the enum object using its name """
        return cls[name]

    @classmethod
    def from_ident(cls, ident: object) -> 'BaseChoice':
        """ Get the enum object using its identifier """
        # noinspection PyArgumentList
        return cls(ident)  # pylint: disable=no-value-for-parameter

    def __str__(self):
        """
        This is mainly required for using this with the django *ChoiceFields.
        Changing this WILL break proper functioning of those fields.
        """
        return str(self.ident)
