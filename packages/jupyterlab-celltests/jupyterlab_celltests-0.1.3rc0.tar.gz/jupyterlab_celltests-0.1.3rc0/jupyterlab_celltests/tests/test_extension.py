# for Coverage
from mock import MagicMock
from jupyterlab_celltests.extension import load_jupyter_server_extension


class TestExtension:
    def test_load_jupyter_server_extension(self):

        m = MagicMock()

        m.web_app.settings = {}
        m.web_app.settings['base_url'] = '/test'
        load_jupyter_server_extension(m)
