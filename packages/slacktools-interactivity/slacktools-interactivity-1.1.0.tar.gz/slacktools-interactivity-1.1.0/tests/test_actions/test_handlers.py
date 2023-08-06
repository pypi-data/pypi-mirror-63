from interactivity import ActionHandler
from interactivity.generics import Payload


class MyAction(ActionHandler):
    def execute(self):
        return


class TestActionHandler:
    def test_action(self, block_actions_request_data):
        payload = Payload(**block_actions_request_data)
        handler = MyAction(payload)
        assert handler.action == block_actions_request_data["actions"][0]
