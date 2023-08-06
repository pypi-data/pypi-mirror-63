"""Module with default marshaler for an action."""

import logging

from lila.core.action import Action, Method


class ActionMarshaler:
    """Class to marshal a single action."""

    def __init__(self, action, marshaler):
        self._action = action
        self._marshaler = marshaler

    def marshal(self):
        """Marshal the action.

        :returns: dictionary with action data.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to marshal an action")

        action_data = {
            "name": self.marshal_name(),
            "class": self.marshal_classes(),
            "method": self.marshal_method(),
            "href": self.marshal_target(),
            "title": self.marshal_title(),
            "type": self.marshal_media_type(),
            "fields": self.marshal_fields(),
            }

        logger.info("Successfully marshaled an action")
        return action_data

    def marshal_name(self):
        """Marshal action's name.

        :returns: string name of the action.
        :raises: :class:ValueError.
        """
        action = self._action
        try:
            name = action.name
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get action's name")
            raise ValueError("Failed to get action's name") from error

        return str(name)

    def marshal_classes(self):
        """Marshal action's classes.

        :returns: list with string names of action's classes.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        action = self._action
        try:
            classes = list(str(class_) for class_ in action.classes)
        except AttributeError as error:
            logger.error("Failed to get action's classes")
            raise ValueError("Failed to get action's classes") from error
        except TypeError as error:
            logger.error("Failed to iterate over action's classes")
            raise ValueError("Failed to iterate over action's classes") from error

        return classes

    def marshal_method(self):
        """Marshal action's method.

        :returns: string value of action's method.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        action = self._action
        try:
            method = str(action.method)
        except AttributeError as error:
            logger.error("Failed to get action's method")
            raise ValueError("Failed to get action's method") from error

        try:
            method = Method(method)
        except ValueError as error:
            logger.error("Action's method is not supported")
            raise ValueError("Action's method is not supported") from error

        return method.value

    def marshal_target(self):
        """Marshal action's target.

        :returns: string target of the action.
        :raises: :class:ValueError.
        """
        action = self._action
        try:
            target = action.target
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get action's target")
            raise ValueError("Failed to get action's target") from error

        return str(target)

    def marshal_title(self):
        """Marshal action's title.

        :returns: string title of the action or None.
        :raises: :class:ValueError.
        """
        action = self._action
        try:
            title = action.title
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get action's title")
            raise ValueError("Failed to get action's title") from error

        if title is not None:
            title = str(title)

        return title

    def marshal_media_type(self):
        """Marshal action's media type.

        :returns: string value of action's media type or None.
        :raises: :class:ValueError.
        """
        action = self._action
        try:
            media_type = action.media_type
        except AttributeError as error:
            logging.getLogger(__name__).error("Failed to get action's media type")
            raise ValueError("Failed to get action's media type") from error

        if media_type is not None:
            media_type = str(media_type)

        return media_type

    def marshal_fields(self):
        """Marshal action's fields.

        :returns: list with marshaled data of action's fields.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        action = self._action
        try:
            action_fields = list(action.fields)
        except AttributeError as error:
            logger.error("Failed to get action's fields")
            raise ValueError("Failed to get action's fields") from error
        except TypeError as error:
            logger.error("Failed to iterate over action's fields")
            raise ValueError("Failed to iterate over action's fields") from error

        marshal_field = self._marshaler.marshal_field

        marshaled_fields = []
        for field in action_fields:
            try:
                field_data = marshal_field(field)
            except Exception as error:
                logger.error("Failed to marshal action's fields")
                raise ValueError("Failed to marshal action's fields") from error

            marshaled_fields.append(field_data)

        return marshaled_fields


class ActionParser:
    """Class to marshal a single action."""

    def __init__(self, data, parser):
        self._data = data
        self._parser = parser

    def parse(self):
        """Parse an action from the data.

        :returns: :class:`Action <lila.core.action.Action>`.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Try to parse an action")

        action_name = self.parse_name()
        action_classes = self.parse_classes()
        action_method = self.parse_method()
        action_target = self.parse_target()
        action_title = self.parse_title()
        action_media_type = self.parse_media_type()
        action_fields = self.parse_fields()

        try:
            action = Action(
                name=action_name,
                classes=action_classes,
                method=action_method,
                target=action_target,
                title=action_title,
                media_type=action_media_type,
                fields=action_fields,
                )
        except Exception as error:
            logger.error("Failed to create an action with provided data")
            raise ValueError("Failed to create an action with provided data") from error
        else:
            logger.info("Successfully parsed an action")

        return action

    def parse_name(self):
        """Parse action's name.

        :returns: string name of the action.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            action_name = self._data["name"]
        except TypeError as error:
            logger.error("Failed to get name from action data")
            raise ValueError("Failed to get name from action data") from error
        except KeyError as error:
            logger.error("Action data do not have required 'name' key")
            raise ValueError("Action data do not have required 'name' key") from error

        return str(action_name)

    def parse_classes(self):
        """Parse action's classes.

        :returns: list with string names of action's classes.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            action_classes = self._data["class"]
        except TypeError as error:
            logger.error("Failed to get classes from action data")
            raise ValueError("Failed to get classes from action data") from error
        except KeyError:
            action_classes = ()

        try:
            action_classes = tuple(str(class_) for class_ in action_classes)
        except TypeError as error:
            logger.error("Failed to iterate over classes from action data")
            raise ValueError("Failed to iterate over classes from action data") from error

        return action_classes

    def parse_method(self):
        """Parse action's method.

        :returns: :class:`Method <lila.core.action.Method>`.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            action_method = self._data["method"]
        except TypeError as error:
            logger.error("Failed to get method from action data")
            raise ValueError("Failed to get method from action data") from error
        except KeyError:
            action_method = Method.GET.value

        try:
            action_method = Method(action_method)
        except ValueError as error:
            logger.error("Action data contain not supported method")
            raise ValueError("Action data contain not supported method") from error

        return action_method

    def parse_target(self):
        """Parse action's target.

        :returns: string target of the action.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            action_target = self._data["href"]
        except TypeError as error:
            logger.error("Failed to get target from action data")
            raise ValueError("Failed to get target from action data") from error
        except KeyError as error:
            logger.error("Action data do not have required 'href' key")
            raise ValueError("Action data do not have required 'href' key") from error

        return str(action_target)

    def parse_title(self):
        """Parse action's title.

        :returns: string title of the action or None.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            action_title = self._data["title"]
        except TypeError as error:
            logger.error("Failed to get title from action data")
            raise ValueError("Failed to get title from action data") from error
        except KeyError:
            action_title = None

        if action_title is not None:
            action_title = str(action_title)

        return action_title

    def parse_media_type(self):
        """Parse action's media type.

        :returns: string value of action's media type or None.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            action_media_type = self._data["type"]
        except TypeError as error:
            logger.error("Failed to get media type from action data")
            raise ValueError("Failed to get media type from action data") from error
        except KeyError:
            action_media_type = None

        if action_media_type is not None:
            action_media_type = str(action_media_type)
        elif self.parse_fields():
            action_media_type = "application/x-www-form-urlencoded"

        return action_media_type

    def parse_fields(self):
        """Parse action's fields.

        :returns: list with parsed action's fields.
        :raises: :class:ValueError.
        """
        logger = logging.getLogger(__name__)

        try:
            action_fields_data = self._data["fields"]
        except TypeError as error:
            logger.error("Failed to get fields data from action data")
            raise ValueError("Failed to get fields data from action data") from error
        except KeyError:
            action_fields_data = ()

        try:
            action_fields_data = list(action_fields_data)
        except TypeError as error:
            logger.error("Failed to iterate over fields data from action data")
            raise ValueError("Failed to iterate over fields data from action data") from error

        parse_field = self._parser.parse_field

        action_fields = []
        for data in action_fields_data:
            try:
                field = parse_field(data)
            except Exception as error:
                logger.error("Failed to parse action's fields")
                raise ValueError("Failed to parse action's fields") from error

            action_fields.append(field)

        return tuple(action_fields)
