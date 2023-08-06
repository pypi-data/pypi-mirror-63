from typing import Union
from ..node import Node
from .program_track_action import ProgramTrackAction, programTrackActionFragment
import json
from ...blocks_action_builder import BlocksActionBuilder

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

    def __set_feedback(self, data, wait_for_feedback=True):
        if not self.action.waits_for_feedback:
            raise RuntimeError(
                "Can't set feedback for this response because its action does not wait for feedback."
            )

        pta = self._context.client.create_program_track_action(data, wait_for_feedback)

        self._context.client.update_program_track_action_response(self.id, pta.id)

        return pta

    def set_feedback_with_data(self, data_json: str, wait_for_feedback=True) -> ProgramTrackAction:
        data = json.loads(data_json.replace("\n", "\\n"))

        return self.__set_feedback(data, wait_for_feedback)

    def set_feedback(
        self, title: str, blocks_action: Union[dict, BlocksActionBuilder], wait_for_feedback=True
    ) -> ProgramTrackAction:
        if isinstance(blocks_action, BlocksActionBuilder):
            blocks_action = blocks_action.build()

        data = {
            "type": "multiStep",
            "steps": [{"name": title, "action": blocks_action}],
        }

        return self.__set_feedback(data, wait_for_feedback)

    def set_no_feedback(self):
        data = {"type": "multiStep", "steps": []}

        self.__set_feedback(data, False)
