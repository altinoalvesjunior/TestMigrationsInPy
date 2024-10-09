from __future__ import annotations

import unittest
from unittest.mock import patch

from asana import Client

from airflow.models import Connection
from airflow.providers.asana.hooks.asana import AsanaHook


class TestAsanaHook(unittest.TestCase):
    """
    Tests for AsanaHook Asana client retrieval
    """
    def test_missing_password_raises(self):
        """
        Test that the Asana hook raises an exception if password not provided in connection.
        :return: None
        """
        with patch.object(AsanaHook, "get_connection", return_value=Connection(conn_type="asana")):
            hook = AsanaHook()
        with self.assertRaises(ValueError):
            hook.get_conn()