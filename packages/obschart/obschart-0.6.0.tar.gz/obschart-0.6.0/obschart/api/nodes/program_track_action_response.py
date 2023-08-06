from ..node import Node
from .program_track_action import ProgramTrackAction, programTrackActionFragment
from gql import gql
import json

programTrackActionResponseFragment = (
    """
fragment ProgramTrackActionResponse on ProgramTrackActionResponse {
    id
    createdAt
    action {
        ...ProgramTrackAction
    }
    response
}
"""
    + programTrackActionFragment
)


class ProgramTrackActionResponse(Node):
    def __init__(self, data, context=None):
        super().__init__(data, context=context)

    @property
    def action(self):
        return ProgramTrackAction(self._data["action"], self._context)

    @property
    def response(self):
        return self._data["response"]

    def set_feedback_with_data(self, data_json):
        data = json.loads(data_json.replace("\n", "\\n"))

        pta = self._context.client.create_program_track_action(data)

        self._context.client.update_program_track_action_response(self.id, pta.id)

        return pta

    def set_feedback(self, title: str, blocks):
        data = {
            "type": "multiStep",
            "steps": [{"name": title, "action": {"type": "blocks", "blocks": blocks}}],
        }

        pta = self._context.client.create_program_track_action(data)

        self._context.client.update_program_track_action_response(self.id, pta.id)

        return pta
