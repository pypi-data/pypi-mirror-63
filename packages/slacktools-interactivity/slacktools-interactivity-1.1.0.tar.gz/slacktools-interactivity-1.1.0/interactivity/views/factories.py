from typing import Union

from interactivity.generics import HandlerFactory, Payload

from .handlers import ViewHandler, ViewSubmissionHandler
from .payloads import ViewPayload

__all__ = ("ViewFactory",)

HandlerT = Union[ViewHandler, ViewSubmissionHandler]


class ViewFactory(HandlerFactory[HandlerT]):
    """
    Requires that the `private_metadata` stored with the view be valid JSON and
    include an attribute called `view_id` that uniquely identifies the view so
    that a handler can be registered for it.
    """

    @classmethod
    def make_payload(cls, request_data: dict) -> ViewPayload:
        return ViewPayload(**request_data)

    @classmethod
    def extract_key(cls, payload: Payload) -> str:
        return payload.metadata["view_id"]
