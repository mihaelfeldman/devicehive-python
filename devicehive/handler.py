from devicehive.api import Info
from devicehive.api import Configuration
from devicehive.api import Device


class Handler(object):
    """Handler class."""

    def __init__(self, transport, token, options):
        self._transport = transport
        self._token = token
        self.options = options

    def get_info(self):
        info = Info(self._transport)
        return info.get()

    def get_cluster_info(self):
        info = Info(self._transport)
        return info.get_cluster_info()

    def create_token(self, user_id, expiration=None, actions=None,
                     network_ids=None, device_ids=None):
        return self._token.create(user_id, expiration, actions, network_ids,
                                  device_ids)

    def refresh_token(self):
        self._token.refresh()
        return self._token.access_token()

    def get_property(self, name):
        configuration = Configuration(self._transport, self._token, name)
        return configuration.get()

    def set_property(self, name, value):
        configuration = Configuration(self._transport, self._token, name, value)
        configuration.save()

    def list_devices(self, **filters):
        device = Device(self._transport, self._token)
        return device.list(**filters)

    def get_device(self, device_id):
        device = Device(self._transport, self._token)
        device.init(device_id)
        if device.id:
            return device

    @staticmethod
    def put_device(device):
        device.save()

    @staticmethod
    def remove_device(device):
        device.remove()

    def handle_connected(self):
        raise NotImplementedError

    def handle_event(self, event):
        raise NotImplementedError