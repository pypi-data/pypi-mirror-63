"""Base handler classes."""

import typing

from abc import ABCMeta, abstractmethod
from typing import (
    Dict,
    Optional,
)

if typing.TYPE_CHECKING:
    from eaf.state import State


class Handler(metaclass=ABCMeta):
    """Base handler."""

    def __init__(self, owner: State):
        self._owner = owner

    @property
    def owner(self) -> State:
        """Handler's owner getter."""

        return self._owner

    @abstractmethod
    def handle(self):
        """Handle event."""

        raise NotImplementedError  # pragma: no cover


class Event:
    QUIT = "quit"
    SIMPLE = "simple"

    def __init__(self, etype):
        self.type = etype


class KeyPressedEvent(Event):

    KEYUP = "keyup"
    KEYDOWN = "keydown"

    def __init__(self, up, scancode):
        super().__init__(self, self.KEYUP if up else self.KEYDOWN)
        self._scancode = scancode

    @property
    def scancode(self):
        return self._scancode


class UserEvent(Event):

    USER = "user"

    def __init__(self, data=None):
        super().__init__(self.USER)

        self._data = data

    @property
    def data(self):
        return self._data


class EventQueue:
    def get_events(self):
        return []


# TODO: remove owner link if it's not needed anymore
class EventHandler(Handler):
    """Base game event handler.

    Handles events using the event queue.
    Provides command mapping manipulations via the default handle() method.
    You must instantiate this class only after application being initialized.
    Application instance has event queue object, that will be used here.

    :param :class:`xoinvader.state.State` owner: handler's owner state
    :param dict command_map: key->command mapping
    """

    def __init__(self, owner: State, command_map: Optional[Dict] = None):
        super().__init__(owner)

        self._command_map = command_map or {}
        # TODO: implement proper queue object
        self._event_queue = owner.app.event_queue

    # TODO: event-handling: I think we need some global event bus in whole
    #       application.
    def event_queue(self):
        """Event queue stub."""

        return [("KEY_PRESS", self.get_input())]

    # TODO: event-handling: abstract getting input from curses
    def get_input(self):
        """Get input from keyboard."""

        return self._event_queue.getch()

    def handle(self):
        """Handle input event."""

        for event in self.event_queue():
            if event[0] == "KEY_PRESS":
                command = self._command_map.get(event[1])
                if callable(command):
                    command()
            else:
                raise ValueError("Unknown event type: {0}".format(event[0]))
