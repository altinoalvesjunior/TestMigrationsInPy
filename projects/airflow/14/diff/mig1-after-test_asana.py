from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from asana import Client
from pytest import param

from airflow.models import Connection
from airflow.providers.asana.hooks.asana import AsanaHook
from tests.test_utils.providers import get_provider_min_airflow_version, object_exists


class TestAsanaHook:
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
        assert type(client) == Client