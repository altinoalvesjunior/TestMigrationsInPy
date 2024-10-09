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
    def test_asana_client_retrieved(self):
        """
        Test that we successfully retrieve an Asana client given a Connection with complete information.
        :return: None
        """
        with patch.object(
            AsanaHook, "get_connection", return_value=Connection(conn_type="asana", password="test")
        ):
            hook = AsanaHook()
        client = hook.get_conn()
        self.assertEqual(type(client), Client)