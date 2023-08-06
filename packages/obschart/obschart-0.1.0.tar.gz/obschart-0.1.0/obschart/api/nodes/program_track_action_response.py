from ..node import Node
from .program_track_action import ProgramTrackAction, programTrackActionFragment
from gql import gql

programTrackActionResponseFragment = '''
fragment ProgramTrackActionResponse on ProgramTrackActionResponse {
    id
    createdAt
    action {
        ...ProgramTrackAction
    }
    response
}
''' + programTrackActionFragment


class ProgramTrackActionResponse(Node):
    def __init__(self, data, context=None):
        super().__init__(data, context=context)

    @property
    def action(self):
        return ProgramTrackAction(self._data['action'], self._context)

    @property
    def response(self):
        return self._data['response']

    def set_feedback(self, title: str, message: str):
        new_block = {
            'type': 'text',
            'content': message
        }
        new_blocks = [new_block]
        new_action = {
            'type': 'blocks',
            'blocks': new_blocks
        }
        new_step = {
            'name': title,
            'action': new_action
        }
        new_steps = [new_step]
        data = {
            'type': 'multiStep',
            'steps': new_steps
        }

        pma = self._context.client.create_program_track_action(data)

        self._context.client.update_program_track_action_response(
            self.id, pma.id)

        return pma
