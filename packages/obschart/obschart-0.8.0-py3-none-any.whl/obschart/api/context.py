class Context(object):
    def __init__(self, client, data={}):
        super().__init__()

        from ..obschart_client import ObschartClient

        self.client: ObschartClient = client
        self.data = data
