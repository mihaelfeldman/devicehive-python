from devicehive import Handler
from devicehive import DeviceHive


class TestHandler(Handler):
    """Test handler class."""

    def handle_connect(self):
        try:
            if not self.options['handle_connect'](self):
                self.api.disconnect()
        except Exception as exception:
            self.options['test'].set_exception(exception)
            self.api.disconnect()

    def handle_event(self, event):
        pass


class Test(object):
    """Test class."""

    def __init__(self, transport_url, refresh_token):
        self._transport_url = transport_url
        self._refresh_token = refresh_token
        self._exception = None

    def set_exception(self, exception):
        self._exception = exception

    def exception(self):
        return self._exception

    def run(self, handle_connect, handle_event=None):
        handler_options = {'test': self,
                           'handle_connect': handle_connect,
                           'handle_event': handle_event}
        device_hive = DeviceHive(self._transport_url, TestHandler,
                                 handler_options)
        device_hive.connect(refresh_token=self._refresh_token)
        device_hive.join()
        exception = self.exception()
        if exception:
            raise exception