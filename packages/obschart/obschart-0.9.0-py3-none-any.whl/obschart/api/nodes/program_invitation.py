from ..node import Node

programInvitationFragment = """
fragment ProgramInvitation on ProgramInvitation {
    id
}
"""


class ProgramInvitation(Node):
    def __init__(self, data, context=None):
        super().__init__(data, context=context)
