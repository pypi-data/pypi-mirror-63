"""Module to work with Siren actions."""

import enum

from lila.core.base import Component
from lila.core.field import Field


@enum.unique
class Method(enum.Enum):
    """Enumerable with supported methods."""
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    DELETE = "DELETE"
    PATCH = "PATCH"

    def __str__(self):
        return self.value


class Action(Component):
    """Class to work with Siren actions."""

    def __init__(
            self,
            name,
            target,
            classes=(),
            method=Method.GET,
            title=None,
            fields=(),
            media_type=None,
        ):
        # pylint: disable=too-many-arguments
        super(Action, self).__init__(classes=classes, title=title)

        self._name = str(name)
        self._target = str(target)

        try:
            self._method = Method(str(method))
        except ValueError:
            raise ValueError("Method '{0}' is not supported".format(method))

        if any(not isinstance(field, Field) for field in fields):
            raise ValueError("Some of the fields are of incompatible type")

        if len(set(field.name for field in fields)) != len(fields):
            raise ValueError("Some of the fields have the same name")

        self._fields = tuple(fields)

        if media_type is not None:
            media_type = str(media_type)
        elif self._fields:
            media_type = "application/x-www-form-urlencoded"
        self._media_type = media_type

    @property
    def name(self):
        """Name of the action."""
        return self._name

    @property
    def target(self):
        """Request target of the action."""
        return self._target

    @property
    def method(self):
        """Method of the action."""
        return self._method

    @property
    def fields(self):
        """Fields to pass to the action."""
        return tuple(self._fields)

    @property
    def media_type(self):
        """Media type of action's payload."""
        return self._media_type
