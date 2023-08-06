import pytest

from interactivity import ActionFactory, ActionHandler


class MyAction(ActionHandler):
    def execute(self):
        return


class TestActionFactory:
    @pytest.fixture(autouse=True)
    def register(self):
        ActionFactory._handlers = {}
        ActionFactory.register_handler("my_id", MyAction)

    def test_register(self, message_action_request_data):
        handler = ActionFactory.make_handler(message_action_request_data)
        assert isinstance(handler, MyAction)
