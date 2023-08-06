from ..node import Node
from gql import gql

tagFragment = """
fragment Tag on Tag {
    id
    name
    slug
    createdAt
}
"""


class Tag(Node):
    def __init__(self, data, context=None):
        super().__init__(data, context=context)

    @property
    def name(self):
        return self._data["name"]

    @property
    def slug(self):
        return self._data["slug"]
