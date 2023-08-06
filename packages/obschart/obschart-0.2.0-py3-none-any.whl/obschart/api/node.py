from typing import Union, Dict, Any
from obschart.api.context import Context


class Node(object):
    def __init__(self, data: Dict[str, Any], context: Union[Context, None] = None):
        super().__init__()

        self._data = data
        self._context = context

    def _execute(self, query, variables):
        if not self._context:
            raise Exception('Expected context')

        return self._context.client._execute(query, variables)

    def __repr__(self):
        return '{} (ID: {}) {}'.format(self.__class__.__name__, self.id, self._data)

    @property
    def id(self):
        return self._data['id']
