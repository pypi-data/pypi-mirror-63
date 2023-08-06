from abc import ABC
from typing import Union

from interactivity.generics import ActivityHandler

from .payloads import ViewClosedPayload, ViewPayload, ViewSubmissionPayload

__all__ = (
    "ViewHandler",
    "ViewSubmissionHandler",
)


class ViewHandler(ActivityHandler[Union[ViewPayload, ViewClosedPayload]], ABC):
    """Base handler class used for view actions."""

    def __init__(self, payload: ViewPayload):
        super().__init__(payload)


class ViewSubmissionHandler(ActivityHandler[ViewSubmissionPayload], ABC):
    def __init__(self, payload: ViewSubmissionPayload):
        super().__init__(payload)
        self.state = self.payload.view["state"]
