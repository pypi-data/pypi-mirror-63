from ..node import Node
from .program_module import ProgramModule
from gql import gql

programTrackActionFragment = """
fragment ProgramTrackAction on ProgramTrackAction {
    id
    sourceProgramModule {
        id
    }
    waitsForFeedback
}
"""


class ProgramTrackAction(Node):
    def __init__(self, data, context=None):
        super().__init__(data, context=context)

    @property
    def waits_for_feedback(self) -> bool:
        return self._data["waitsForFeedback"]

    @property
    def module(self):
        if not self._data["sourceProgramModule"]:
            return None

        return ProgramModule(self._data["sourceProgramModule"], self._context)

    @property
    def responses(self):
        from .program_track_action_response import (
            ProgramTrackActionResponse,
            programTrackActionResponseFragment,
        )

        query = gql(
            """
          query ProgramTrackActionResponsesQuery($programTrackActionId: ID)  {
            programTrackAction(id: $programTrackActionId) {
              responses(first: 9999) {
                edges {
                  node {
                    ...ProgramTrackActionResponse
                  }
                }
              }
            }
          }
          """
            + programTrackActionResponseFragment
        )

        variables = {}
        variables["programTrackActionId"] = self.id
        response = self._execute(query, variables)

        responses: list[ProgramTrackActionResponse] = []
        for edge in response["programTrackAction"]["responses"]["edges"]:
            responses.append(ProgramTrackActionResponse(edge["node"], self._context))

        return responses

    async def poll_responses(self):
        return await self._context.client.poll_program_track_action_responses(
            {"programTrackActionId": {"eq": self.id}}
        )

    async def wait_for_response(self):
        responses = await self.poll_responses()
        return responses[0]

    # def add_step(self, step_name: str, text_block_content: str):
    #     query = gql('''
    #         query ProgramTrackActionAddStepQuery($id: ID) {
    #             programTrackAction(id: $id) {
    #                 data
    #             }
    #         }
    #     ''')

    #     variables = {}
    #     variables['id'] = self.id
    #     response = self._context.client._execute(query, variables)

    #     program_module_data_action = response['programTrackAction']['data']

    #     new_block = {
    #         'type': 'text',
    #         'content': text_block_content
    #     }
    #     new_blocks = [new_block]
    #     new_action = {
    #         'type': 'blocks',
    #         'blocks': new_blocks
    #     }
    #     new_step = {
    #         'name': step_name,
    #         'action': new_action
    #     }
    #     program_module_data_action['steps'].append(new_step)

    #     query = gql('''
    #         mutation ProgramTrackActionAddStepMutation($input: UpdateProgramTrackActionInput!)  {
    #             updateProgramTrackAction(input: $input) {
    #                 programTrackAction {
    #                     id
    #                 }
    #             }
    #         }
    #     ''')

    #     variables = {}
    #     variables['input'] = {}
    #     variables['input']['id'] = self.id
    #     variables['input']['data'] = program_module_data_action
    #     self._context.client._execute(query, variables)
