import pytest

from interactivity import ViewFactory, ViewHandler


class MyView(ViewHandler):
    def execute(self):
        return


class TestViewFactory:
    @pytest.fixture(autouse=True)
    def register(self):
        ViewFactory._handlers = {}
        ViewFactory.register_handler("my_view", MyView)

    def test_register(self, view_submission_request_data):
        handler = ViewFactory.make_handler(view_submission_request_data)
        assert isinstance(handler, MyView)
