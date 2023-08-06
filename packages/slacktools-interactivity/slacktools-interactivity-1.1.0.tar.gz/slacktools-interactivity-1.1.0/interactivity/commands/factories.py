from typing import Union

from interactivity.generics import HandlerFactory, Payload

from .handlers import ActionCommandHandler, CommandHandler

__all__ = ("CommandFactory",)


HandlerT = Union[CommandHandler, ActionCommandHandler]


class CommandFactory(HandlerFactory[HandlerT]):
    """Factory that initializes a `CommandHandler` using the Slack request payload."""

    @classmethod
    def extract_key(cls, payload: Payload) -> str:
        return payload.command
