from abc import ABC
from typing import Any, Dict, TypeVar

from interactivity.generics import ActivityHandler, Payload

__all__ = ("ActionHandler",)

P = TypeVar("P", bound=Payload)


class ActionHandler(ActivityHandler[Payload], ABC):
    """
    Base handler class used for block and attachment actions:
    https://api.slack.com/reference/interaction-payloads/block-actions
    """

    def __init__(self, *args, **kwargs):
        """
        Just like `ActionFactory`, assumes that a single action is submitted at a time.
        """
        super(ActionHandler, self).__init__(*args, **kwargs)
        self.action: Dict[str, Any] = self.payload.actions[0]
