from . import protocols
from .client_types import HTTPClient, DBClient
from .exceptions import ServiceTypeException


class Service:
    """
    SERVICE class to wrap external services that your application uses

    >>> some_http_service = Service('external data provider', 'http')
    >>> query = some_http_service.client.fetch_data('https://randomuser.me/api/')
    >>> if not query.errors:
    ...     print(type(query.data))
    <class 'dict'>
    """

    instances = 0

    def __init__(self, name, protocol):
        if not isinstance(name, str):
            raise ServiceTypeException('Name of service must be a string!')
        self.name = name
        if protocol is protocols.HTTP:
            self.client = HTTPClient(name)
        elif protocol is protocols.DB:
            # self.client = DBClient()
            raise NotImplementedError
        else:
            raise ServiceTypeException('Invalid protocol type of client: Use e.g. protocols.DB')
        self.instances += 1

    def register(self, path, *args, **kwargs):
        def wrapped(**params):
            q = self.client.fetch_data(path.format(**params), *args, **kwargs)
            return q
        return wrapped

    def __str__(self):
        return '{name} Service'.format(name=self.name)

    def __repr__(self):
        return 'Name: {name}, Type: {client}, Instances: {instances}'.format(name=self.name,
                                                                             client=self.client,
                                                                             instances=self.instances)

