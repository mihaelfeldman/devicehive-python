from devicehive.api_request import AuthApiRequest
from devicehive.api_request import ApiRequestError


class Network(object):
    """Network class."""

    ID_KEY = 'id'
    NAME_KEY = 'name'
    DESCRIPTION_KEY = 'description'

    def __init__(self, api, network=None):
        self._api = api
        self._id = None
        self.name = None
        self.description = None
        if network:
            self._init(network)

    def _init(self, device):
        self._id = device[self.ID_KEY]
        self.name = device[self.NAME_KEY]
        self.description = device[self.DESCRIPTION_KEY]

    def _ensure_exists(self):
        if self._id:
            return
        raise NetworkError('Network does not exist.')

    @property
    def id(self):
        return self._id

    def get(self, network_id):
        auth_api_request = AuthApiRequest(self._api)
        auth_api_request.url('network/{id}', id=network_id)
        auth_api_request.action('network/get')
        auth_api_request.response_key('network')
        network = auth_api_request.execute('Network get failure.')
        self._init(network)

    def save(self):
        self._ensure_exists()
        network = {self.ID_KEY: self._id,
                   self.NAME_KEY: self.name,
                   self.DESCRIPTION_KEY: self.description}
        auth_api_request = AuthApiRequest(self._api)
        auth_api_request.method('PUT')
        auth_api_request.url('network/{id}', id=self._id)
        auth_api_request.action('network/update')
        auth_api_request.set('network', network, True)
        auth_api_request.execute('Network save failure.')


class NetworkError(ApiRequestError):
    """Network error."""
