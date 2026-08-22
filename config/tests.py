import importlib
import sys
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase


class SettingsTests(SimpleTestCase):
    def test_settings_requires_django_secret_key(self):
        sys.modules.pop("config.settings", None)
        self.addCleanup(self._reload_settings)

        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ImproperlyConfigured):
                importlib.import_module("config.settings")

    def _reload_settings(self):
        importlib.import_module("config.settings")


class WsgiTests(SimpleTestCase):
    def test_wsgi_application_exists(self):
        from config.wsgi import application

        self.assertIsNotNone(application)
