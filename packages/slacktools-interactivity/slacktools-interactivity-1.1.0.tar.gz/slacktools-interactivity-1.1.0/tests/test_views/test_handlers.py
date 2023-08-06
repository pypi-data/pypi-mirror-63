from interactivity import ViewSubmissionHandler
from interactivity.generics import Payload


class MyView(ViewSubmissionHandler):
    def execute(self):
        return


class TestViewSubmissionHandler:
    def test_state(self, view_submission_request_data):
        payload = Payload(**view_submission_request_data)
        handler = MyView(payload)
        assert handler.state == payload.view["state"]
