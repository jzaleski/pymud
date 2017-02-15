class BaseProcessor(object):
    def __init__(self, client_connection):
        self._client_connection = client_connection
