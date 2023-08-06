from ..node import Node


class Session(Node):
    def __init__(self, data, context=None):
        super().__init__(data, context=context)
