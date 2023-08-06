from typing import Optional, Dict, Any
from .context import Context


class Node(object):
    _data: dict
    _context: Optional[Context]

    def __init__(self, data: Dict[str, Any], context: Optional[Context] = None):
        super().__init__()

        self._data = data
        self._context = context

    def _execute(self, query, variables):
        if not self._context:
            raise Exception("Expected context")

        return self._context.client._execute(query, variables)

    def __repr__(self):
        return f"{self.__class__.__name__} (ID: {self.id}) {self._data}"

    @property
    def id(self):
        return self._data["id"]
