from gql import gql, Client
from .gql_client_transport import GqlClientTransport
from .api.nodes import (
    Session,
    Image,
    imageFragment,
    ProgramInvitation,
    ProgramTrackActionResponse,
    programTrackActionResponseFragment,
    ProgramTrackAction,
    programTrackActionFragment,
    ProgramModule,
    programModuleFragment,
    Tag,
    tagFragment,
)
from .api.context import Context
from typing import Optional, Dict, Any, Callable
import datetime
from .blocks_action_builder import BlocksActionBuilder
from typing import Union, Awaitable
import asyncio
import traceback


OnResponseCallback = Callable[[ProgramTrackActionResponse], Awaitable[None]]


class ObschartClient:
    def __init__(
        self,
        authentication_token: Optional[str] = None,
        api_url: Optional[str] = "https://api.obschart.com/",
    ):
        super().__init__()

        transport = GqlClientTransport(api_url)
        self.gql_client = Client(transport=transport)
        self._context = Context(self)

        if authentication_token:
            self.set_authentication_token(authentication_token)

    def set_authentication_token(self, authentication_token: str):
        self.gql_client.transport.headers = self.gql_client.transport.headers or {}
        self.gql_client.transport.headers["Authorization"] = f"Bearer {authentication_token}"

    def _execute(self, query, variables: Optional[Dict[str, Any]] = None):
        return self.gql_client.execute(query, variables)

    def _execute_mutation(self, query, input: Optional[Dict[str, Any]] = None):
        variables = {"input": input}
        return self._execute(query, variables)

    def login(self, email: str, password: str):
        query = gql(
            """
          mutation CreateSessionMutation($input: CreateSessionInput) {
            createSession(input: $input) {
              token
              session {
                id
              }
            }
          }
          """
        )

        input = {"password": password, "email": email}
        result = self._execute_mutation(query, input)

        authentication_token = result["createSession"]["token"]
        self.set_authentication_token(authentication_token)

        return Session(result["createSession"]["session"], Context(self))

    async def poll_program_track_action_responses(self, filter: dict):
        query = gql(
            """
          query OnResponseQuery($filter: ProgramTrackActionResponseFilterInput) {
            programTrackActionResponses(filter: $filter, first: 9999) {
              edges {
                node {
                  ...ProgramTrackActionResponse
                }
              }
            }
          }
        """
            + programTrackActionResponseFragment
        )

        filter = filter.copy()
        now = datetime.datetime.utcnow()
        filter.update(
            {"createdAt": {"after": now.replace(tzinfo=datetime.timezone.utc).isoformat()}}
        )
        variables = {"filter": filter}

        while True:
            try:
                response = self._execute(query, variables)
                edges = response["programTrackActionResponses"]["edges"]

                if len(edges) > 0:
                    break
            except Exception as exception:
                traceback.print_exception(None, exception, exception.__traceback__)

            await asyncio.sleep(1)

        responses: list[ProgramTrackActionResponse] = [
            ProgramTrackActionResponse(edge["node"], self._context) for edge in edges
        ]

        return responses

    def on_response(self, on_response_callback: OnResponseCallback):
        async def main() -> Any:
            while True:
                responses = await self.poll_program_track_action_responses(
                    {"applicationId": {"eq": "me"}}
                )

                results = await asyncio.gather(
                    *[on_response_callback(response) for response in responses],
                    return_exceptions=True,
                )

                for result in results:
                    if isinstance(result, Exception):
                        exception = result
                        traceback.print_exception(None, exception, exception.__traceback__)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

    def create_program_track_action(self, data: Any, waits_for_feedback: bool):
        query = gql(
            """
          mutation CreateProgramTrackActionMutation($input: CreateProgramTrackActionInput!) {
            createProgramTrackAction(input: $input) {
              programTrackAction  {
                ...ProgramTrackAction
              }
            }
          }
          """
            + programTrackActionFragment
        )

        input = {"data": data, "waitsForFeedback": waits_for_feedback}
        result = self._execute_mutation(query, input)

        return ProgramTrackAction(
            result["createProgramTrackAction"]["programTrackAction"], self._context
        )

    def create_image(self, image: Union[str, Any]):
        query = gql(
            """
          mutation CreateImageMutation($input: CreateImageInput!) {
            createImage(input: $input) {
              image  {
                ...Image
              }
            }
          }
          """
            + imageFragment
        )

        if isinstance(image, str):
            image = open(image, "rb")

        input = {"image": image}
        result = self._execute_mutation(query, input)

        return Image(result["createImage"]["image"], self._context)

    def create_program_invitation(self, program_id: str):
        query = gql(
            """
          mutation CreateProgramInvitationMutation($input: CreateProgramInvitationInput!) {
            createProgramInvitation(input: $input) {
              programInvitation  {
                id
              }
            }
          }
          """
        )

        input = {"programId": program_id}
        result = self._execute_mutation(query, input)

        return ProgramInvitation(
            result["createProgramInvitation"]["programInvitation"], self._context
        )

    def send_program_invitation_sms(self, program_invitation_id: str, phone_number: str):
        query = gql(
            """
          mutation SendProgramInvitationSmsMutation($input: SendProgramInvitationSmsInput) {
            sendProgramInvitationSms(input: $input) {
              programInvitation  {
                id
              }
            }
          }
          """
        )

        input = {"id": program_invitation_id, "phoneNumber": phone_number}
        result = self._execute(query, input)

        return ProgramInvitation(
            result["sendProgramInvitationSms"]["programInvitation"], self._context
        )

    def get_current_session(self):
        query = gql(
            """
          query CurrentSessionQuery {
            currentSession {
              id
              user {
                id
                name
                email
              }
            }
          }
          """
        )

        result = self._execute(query)

        return Session(result["currentSession"], self._context)

    def get_program_track_action_response(self, id):
        query = gql(
            """
          query ProgramTrackActionResponseQuery($id: ID) {
            programTrackActionResponse(id: $id) {
              ...ProgramTrackActionResponse
            }
          }
          """
            + programTrackActionResponseFragment
        )

        variables = {"id": id}
        result = self._execute(query, variables)

        return ProgramTrackActionResponse(result["programTrackActionResponse"], self._context)

    def update_program_track_action_response(self, id: str, feedback_program_track_action_id: str):
        query = gql(
            """
            mutation UpdateProgramTrackActionResponseMutation($input: UpdateProgramTrackActionResponseInput!)  {
                updateProgramTrackActionResponse(input: $input) {
                    programTrackActionResponse {
                        ...ProgramTrackActionResponse
                    }
                }
            }
        """
            + programTrackActionResponseFragment
        )

        input = {
            "id": id,
            "feedbackProgramTrackActionId": feedback_program_track_action_id,
        }
        result = self._context.client._execute_mutation(query, input)

        return ProgramTrackActionResponse(
            result["updateProgramTrackActionResponse"]["programTrackActionResponse"], self._execute,
        )

    def build_feedback_data(self):
        return BlocksActionBuilder()

    async def list_program_modules(self, filter: dict):
        query = gql(
            """
          query ListProgramModules($filter: ProgramModuleFilterInput) {
            programModules(filter: $filter, first: 9999) {
              edges {
                node {
                  ...ProgramModule
                }
              }
            }
          }
        """
            + programModuleFragment
        )

        variables = {"filter": filter}
        response = self._execute(query, variables)

        nodes: list[ProgramModule] = [
            ProgramModule(edge["node"], self._context)
            for edge in response["programModules"]["edges"]
        ]

        return nodes

    async def list_tags(self, filter: dict):
        query = gql(
            """
          query ListTags($filter: TagFilterInput) {
            tags(filter: $filter, first: 9999) {
              edges {
                node {
                  ...Tag
                }
              }
            }
          }
        """
            + tagFragment
        )

        variables = {"filter": filter}
        response = self._execute(query, variables)

        nodes: list[Tag] = [Tag(edge["node"], self._context) for edge in response["tags"]["edges"]]

        return nodes

    def update_program_module(self, id: str, is_public: bool):
        query = gql(
            """
            mutation UpdateProgramModuleMutation($input: UpdateProgramModuleInput!)  {
                updateProgramModule(input: $input) {
                    programModule {
                        ...ProgramModule
                    }
                }
            }
        """
            + programModuleFragment
        )

        input = {
            "id": id,
            "isPublic": is_public,
        }
        result = self._context.client._execute_mutation(query, input)

        return ProgramModule(result["updateProgramModule"]["programModule"], self._execute,)

