import json

from interactivity.generics import Payload

__all__ = ("ViewPayload",)


class ViewPayload(Payload):
    """
    Requires that the value provided for `private_metadata` by the view be
    valid JSON and contain an attribute called `view_id`.

    https://api.slack.com/reference/interaction-payloads/views
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.metadata = json.loads(self.view["private_metadata"])
