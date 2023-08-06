from abc import ABC

from interactivity.generics import ActivityHandler

from .payloads import ViewPayload

__all__ = (
    "ViewHandler",
    "ViewSubmissionHandler",
)


class ViewHandler(ActivityHandler[ViewPayload], ABC):
    """Base handler class used for view actions."""

    def __init__(self, payload: ViewPayload):
        super().__init__(payload)


class ViewSubmissionHandler(ViewHandler, ABC):
    def __init__(self, payload: ViewPayload):
        super().__init__(payload)
        self.state = self.payload.view["state"]
