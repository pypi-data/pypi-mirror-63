from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
from obschart.api.nodes import Session, ProgramInvitation, ProgramTrackActionResponse, programTrackActionResponseFragment, ProgramTrackAction, programTrackActionFragment
from obschart.api.context import Context
from typing import Optional, Dict, Any, Callable
import polling
import datetime

OnResponseCallback = Callable[[ProgramTrackActionResponse], None]


class ObschartClient:
    def __init__(self, authentication_token: Optional[str] = None, api_url: Optional[str] = 'https://api.obschart.com/'):
        super().__init__()

        transport = RequestsHTTPTransport(api_url, use_json=True)
        self.gql_client = Client(transport=transport)
        self._context = Context(self)

        if authentication_token:
            self.set_authentication_token(authentication_token)

    def set_authentication_token(self, authentication_token: str):
        self.gql_client.transport.headers = self.gql_client.transport.headers or {}
        self.gql_client.transport.headers['Authorization'] = 'Bearer {}'.format(
            authentication_token)

    def _execute(self, query, variables: Optional[Dict[str, Any]] = None):
        variable_values = None

        if variables:
            variable_values = json.dumps(variables)

        return self.gql_client.execute(
            query, variable_values)

    def _execute_mutation(self, query, input: Optional[Dict[str, Any]] = None):
        variables = {
            'input': input
        }
        return self._execute(query, variables)

    def login(self, email: str, password: str):
        query = gql('''
          mutation CreateSessionMutation($input: CreateSessionInput) {
            createSession(input: $input) {
              token
              session {
                id
              }
            }
          }
          ''')

        input = {
            'password': password,
            'email': email
        }
        result = self._execute_mutation(
            query, input)

        authentication_token = result['createSession']['token']
        self.set_authentication_token(authentication_token)

        return Session(result['createSession']['session'], Context(self))

    def poll_program_track_action_responses(self, filter):
        time = datetime.datetime.utcnow()

        query = gql('''
          query OnResponseQuery($filter: ProgramTrackActionResponseFilterInput) {
            programTrackActionResponses(filter: $filter, first: 9999) {
              edges {
                node {
                  ...ProgramTrackActionResponse
                }
              }
            }
          }
        ''' + programTrackActionResponseFragment)

        filter = filter.copy()
        filter.update({
            'createdAt': {
                'after': time.replace(
                    tzinfo=datetime.timezone.utc).isoformat()
            }
        })
        variables = {
            'filter': filter
        }

        def poll():
            # print('Polling...')
            return self._execute(query, variables)

        def check_success(response):
            return len(response['programTrackActionResponses']['edges']) > 0

        response = polling.poll(
            poll,
            check_success=check_success,
            step=1,
            poll_forever=True
        )

        responses: list[ProgramTrackActionResponse] = []
        for edge in response['programTrackActionResponses']['edges']:
            responses.append(ProgramTrackActionResponse(
                edge['node'], self._context))

        return responses

    def on_response(self, on_response_callback: OnResponseCallback):
        responses = self.poll_program_track_action_responses({
            'applicationId': {'eq': 'me'}
        })

        for response in responses:
            on_response_callback(response)

        return self.on_response(on_response_callback)

    def create_program_track_action(self, data: Any):
        query = gql('''
          mutation CreateProgramTrackActionMutation($input: CreateProgramTrackActionInput!) {
            createProgramTrackAction(input: $input) {
              programTrackAction  {
                ...ProgramTrackAction
              }
            }
          }
          ''' + programTrackActionFragment)

        input = {
            'data': data
        }
        result = self._execute_mutation(
            query, input)

        return ProgramTrackAction(result['createProgramTrackAction']['programTrackAction'], self._context)

    def create_program_invitation(self, program_id: str):
        query = gql('''
          mutation CreateProgramInvitationMutation($input: CreateProgramInvitationInput!) {
            createProgramInvitation(input: $input) {
              programInvitation  {
                id
              }
            }
          }
          ''')

        input = {
            'programId': program_id
        }
        result = self._execute_mutation(
            query, input)

        return ProgramInvitation(result['createProgramInvitation']['programInvitation'], self._context)

    def send_program_invitation_sms(self, program_invitation_id: str, phone_number: str):
        query = gql('''
          mutation SendProgramInvitationSmsMutation($input: SendProgramInvitationSmsInput) {
            sendProgramInvitationSms(input: $input) {
              programInvitation  {
                id
              }
            }
          }
          ''')

        input = {
            'id':  program_invitation_id,
            'phoneNumber':  phone_number
        }
        result = self._execute(
            query, input)

        return ProgramInvitation(result['sendProgramInvitationSms']['programInvitation'], self._context)

    def get_current_session(self):
        query = gql('''
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
          ''')

        result = self._execute(query)

        return Session(result['currentSession'], self._context)

    def get_program_track_action_response(self, id):
        query = gql('''
          query ProgramTrackActionResponseQuery($id: ID) {
            programTrackActionResponse(id: $id) {
              ...ProgramTrackActionResponse
            }
          }
          ''' + programTrackActionResponseFragment)

        variables = {
            'id': id
        }
        result = self._execute(query, variables)

        return ProgramTrackActionResponse(result['programTrackActionResponse'], self._context)

    def update_program_track_action_response(self, id: str, feedback_program_track_action_id: str):
        query = gql('''
            mutation UpdateProgramTrackActionResponseMutation($input: UpdateProgramTrackActionResponseInput!)  {
                updateProgramTrackActionResponse(input: $input) {
                    programTrackActionResponse {
                        ...ProgramTrackActionResponse
                    }
                }
            }
        ''' + programTrackActionResponseFragment)

        input = {
            'id': id,
            'feedbackProgramTrackActionId': feedback_program_track_action_id
        }
        result = self._context.client._execute_mutation(query, input)

        return ProgramTrackActionResponse(result['updateProgramTrackActionResponse']['programTrackActionResponse'], self._execute)
